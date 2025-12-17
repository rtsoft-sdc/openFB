import os 
import sys
import cv2
import numpy as np
import logging
from shared_memory_dict import SharedMemoryDict
from time import sleep



import platform
from rknnlite.api import RKNNLite

from copy import copy
import os
import cv2
import json

class Letter_Box_Info():
    def __init__(self, shape, new_shape, w_ratio, h_ratio, dw, dh, pad_color) -> None:
        self.origin_shape = shape
        self.new_shape = new_shape
        self.w_ratio = w_ratio
        self.h_ratio = h_ratio
        self.dw = dw 
        self.dh = dh
        self.pad_color = pad_color




class COCO_test_helper():
    def __init__(self, enable_letter_box = False) -> None:
        self.record_list = []
        self.enable_ltter_box = enable_letter_box
        if self.enable_ltter_box is True:
            self.letter_box_info_list = []
        else:
            self.letter_box_info_list = None

    def letter_box(self, im, new_shape, pad_color=(0,0,0), info_need=False):
        # Resize and pad image while meeting stride-multiple constraints
        shape = im.shape[:2]  # current shape [height, width]
        logging.error(f"INITIAL SHAPE: {shape}")
        if isinstance(new_shape, int):
            new_shape = (new_shape, new_shape)

        # Scale ratio
        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])

        # Compute padding
        ratio = r  # width, height ratios
        new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
        dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding

        dw /= 2  # divide padding into 2 sides
        dh /= 2

        if shape[::-1] != new_unpad:  # resize
            im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=pad_color)  # add border
        
        if self.enable_ltter_box is True:
            self.letter_box_info_list.append(Letter_Box_Info(shape, new_shape, ratio, ratio, dw, dh, pad_color))
        if info_need is True:
            return im, ratio, (dw, dh)
        else:
            return im

    def direct_resize(self, im, new_shape, info_need=False):
        shape = im.shape[:2]
        h_ratio = new_shape[0]/ shape[0]
        w_ratio = new_shape[1]/ shape[1]
        if self.enable_ltter_box is True:
            self.letter_box_info_list.append(Letter_Box_Info(shape, new_shape, w_ratio, h_ratio, 0, 0, (0,0,0)))
        im = cv2.resize(im, (new_shape[1], new_shape[0]))
        return im

    def get_real_box(self, box, in_format='xyxy'):
        bbox = copy(box)
        if self.enable_ltter_box == True:
        # unletter_box result
            if in_format=='xyxy':
                bbox[:,0] -= self.letter_box_info_list[-1].dw
                bbox[:,0] /= self.letter_box_info_list[-1].w_ratio
                bbox[:,0] = np.clip(bbox[:,0], 0, self.letter_box_info_list[-1].origin_shape[1])

                bbox[:,1] -= self.letter_box_info_list[-1].dh
                bbox[:,1] /= self.letter_box_info_list[-1].h_ratio
                bbox[:,1] = np.clip(bbox[:,1], 0, self.letter_box_info_list[-1].origin_shape[0])

                bbox[:,2] -= self.letter_box_info_list[-1].dw
                bbox[:,2] /= self.letter_box_info_list[-1].w_ratio
                bbox[:,2] = np.clip(bbox[:,2], 0, self.letter_box_info_list[-1].origin_shape[1])

                bbox[:,3] -= self.letter_box_info_list[-1].dh
                bbox[:,3] /= self.letter_box_info_list[-1].h_ratio
                bbox[:,3] = np.clip(bbox[:,3], 0, self.letter_box_info_list[-1].origin_shape[0])
        return bbox

    def get_real_seg(self, seg):
        #! fix side effect
        dh = int(self.letter_box_info_list[-1].dh)
        dw = int(self.letter_box_info_list[-1].dw)
        origin_shape = self.letter_box_info_list[-1].origin_shape
        new_shape = self.letter_box_info_list[-1].new_shape
        if (dh == 0) and (dw == 0) and origin_shape == new_shape:
            return seg
        elif dh == 0 and dw != 0:
            seg = seg[:, :, dw:-dw] # a[0:-0] = []
        elif dw == 0 and dh != 0 : 
            seg = seg[:, dh:-dh, :]
        seg = np.where(seg, 1, 0).astype(np.uint8).transpose(1,2,0)
        seg = cv2.resize(seg, (origin_shape[1], origin_shape[0]), interpolation=cv2.INTER_LINEAR)
        if len(seg.shape) < 3:
            return seg[None,:,:]
        else:
            return seg.transpose(2,0,1)

    def add_single_record(self, image_id, category_id, bbox, score, in_format='xyxy', pred_masks = None):
        if self.enable_ltter_box == True:
        # unletter_box result
            if in_format=='xyxy':
                bbox[0] -= self.letter_box_info_list[-1].dw
                bbox[0] /= self.letter_box_info_list[-1].w_ratio

                bbox[1] -= self.letter_box_info_list[-1].dh
                bbox[1] /= self.letter_box_info_list[-1].h_ratio

                bbox[2] -= self.letter_box_info_list[-1].dw
                bbox[2] /= self.letter_box_info_list[-1].w_ratio

                bbox[3] -= self.letter_box_info_list[-1].dh
                bbox[3] /= self.letter_box_info_list[-1].h_ratio
                # bbox = [value/self.letter_box_info_list[-1].ratio for value in bbox]

        if in_format=='xyxy':
        # change xyxy to xywh
            bbox[2] = bbox[2] - bbox[0]
            bbox[3] = bbox[3] - bbox[1]
        else:
            assert False, "now only support xyxy format, please add code to support others format"
        
        def single_encode(x):
            from pycocotools.mask import encode
            rle = encode(np.asarray(x[:, :, None], order="F", dtype="uint8"))[0]
            rle["counts"] = rle["counts"].decode("utf-8")
            return rle

        if pred_masks is None:
            self.record_list.append({"image_id": image_id,
                                    "category_id": category_id,
                                    "bbox":[round(x, 3) for x in bbox],
                                    'score': round(score, 5),
                                    })
        else:
            rles = single_encode(pred_masks)
            self.record_list.append({"image_id": image_id,
                                    "category_id": category_id,
                                    "bbox":[round(x, 3) for x in bbox],
                                    'score': round(score, 5),
                                    'segmentation': rles,
                                    })
    
    def export_to_json(self, path):
        with open(path, 'w') as f:
            json.dump(self.record_list, f)


DEVICE_COMPATIBLE_NODE = '/proc/device-tree/compatible'

def get_host():
    # get platform and device type
    system = platform.system()
    machine = platform.machine()
    os_machine = system + '-' + machine
    if os_machine == 'Linux-aarch64':
        try:
            with open(DEVICE_COMPATIBLE_NODE) as f:
                device_compatible_str = f.read()
                if 'rk3588' in device_compatible_str:
                    host = 'RK3588'
                elif 'rk3562' in device_compatible_str:
                    host = 'RK3562'
                else:
                    host = 'RK3566_RK3568'
        except IOError:
            print('Read device node {} failed.'.format(DEVICE_COMPATIBLE_NODE))
            exit(-1)
    else:
        host = os_machine
    return host

class RKNN_model_container():
    def __init__(self, model_path, target=None, device_id=None) -> None:
        rknn = RKNNLite()

        # Direct Load RKNN Model
        rknn.load_rknn(model_path)
        host_name = get_host()
        # Init runtime environment
        print('--> Init runtime environment')
        # run on RK356x/RK3588 with Debian OS, do not need specify target.
        if host_name == 'RK3588':
            # For RK3588, specify which NPU core the model runs on through the core_mask parameter.
            ret = rknn.init_runtime(core_mask=RKNNLite.NPU_CORE_0)
        else:
            ret = rknn.init_runtime()
        if ret != 0:
            print('Init runtime environment failed')
            exit(ret)
        print('done')
        
        self.rknn = rknn

    def __del__(self):
        del self.rknn

    def run(self, inputs):
        if self.rknn is None:
            print("ERROR: rknn has been released")
            return []

        if isinstance(inputs, list) or isinstance(inputs, tuple):
            pass

        inputs = inputs[:,:,:,None].transpose((-1,0,1,2))
        logging.error(f'SHAPE: {inputs.shape}')
        result = self.rknn.inference(inputs=[inputs])
    
        return result

    def release(self):
        self.rknn.release()
        self.rknn = None

def filter_boxes(boxes, box_confidences, box_class_probs, obj_thresh):
    """Filter boxes with object threshold.
    """
    box_confidences = box_confidences.reshape(-1)
    candidate, class_num = box_class_probs.shape

    class_max_score = np.max(box_class_probs, axis=-1)
    classes = np.argmax(box_class_probs, axis=-1)

    if class_num==1:
        _class_pos = np.where(box_confidences >= obj_thresh)
        scores = (box_confidences)[_class_pos]
    else:
        _class_pos = np.where(class_max_score* box_confidences >= obj_thresh)
        scores = (class_max_score* box_confidences)[_class_pos]

    boxes = boxes[_class_pos]
    classes = classes[_class_pos]

    return boxes, classes, scores

def nms_boxes(boxes, scores, nms_thresh=0.45):
    """Suppress non-maximal boxes.
    # Returns
        keep: ndarray, index of effective boxes.
    """
    x = boxes[:, 0]
    y = boxes[:, 1]
    w = boxes[:, 2] - boxes[:, 0]
    h = boxes[:, 3] - boxes[:, 1]

    areas = w * h
    order = scores.argsort()[::-1]

    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)

        xx1 = np.maximum(x[i], x[order[1:]])
        yy1 = np.maximum(y[i], y[order[1:]])
        xx2 = np.minimum(x[i] + w[i], x[order[1:]] + w[order[1:]])
        yy2 = np.minimum(y[i] + h[i], y[order[1:]] + h[order[1:]])

        w1 = np.maximum(0.0, xx2 - xx1 + 0.00001)
        h1 = np.maximum(0.0, yy2 - yy1 + 0.00001)
        inter = w1 * h1

        ovr = inter / (areas[i] + areas[order[1:]] - inter)
        inds = np.where(ovr <= nms_thresh)[0]
        order = order[inds + 1]
    keep = np.array(keep)
    return keep


def box_process(position, anchors, img_size = (640, 640)):
    grid_h, grid_w = position.shape[2:4]
    col, row = np.meshgrid(np.arange(0, grid_w), np.arange(0, grid_h))
    col = col.reshape(1, 1, grid_h, grid_w)
    row = row.reshape(1, 1, grid_h, grid_w)
    grid = np.concatenate((col, row), axis=1)
    stride = np.array([img_size[1]//grid_h, img_size[0]//grid_w]).reshape(1,2,1,1)

    col = col.repeat(len(anchors), axis=0)
    row = row.repeat(len(anchors), axis=0)
    anchors = np.array(anchors)
    anchors = anchors.reshape(*anchors.shape, 1, 1)

    box_xy = position[:,:2,:,:]*2 - 0.5
    box_wh = pow(position[:,2:4,:,:]*2, 2) * anchors

    box_xy += grid
    box_xy *= stride
    box = np.concatenate((box_xy, box_wh), axis=1)

    # Convert [c_x, c_y, w, h] to [x1, y1, x2, y2]
    xyxy = np.copy(box)
    xyxy[:, 0, :, :] = box[:, 0, :, :] - box[:, 2, :, :]/ 2  # top left x
    xyxy[:, 1, :, :] = box[:, 1, :, :] - box[:, 3, :, :]/ 2  # top left y
    xyxy[:, 2, :, :] = box[:, 0, :, :] + box[:, 2, :, :]/ 2  # bottom right x
    xyxy[:, 3, :, :] = box[:, 1, :, :] + box[:, 3, :, :]/ 2  # bottom right y

    return xyxy

def post_process(input_data, anchors, obj_thresh):
    boxes, scores, classes_conf = [], [], []
    # 1*255*h*w -> 3*85*h*w
    input_data = [_in.reshape([len(anchors[0]),-1]+list(_in.shape[-2:])) for _in in input_data]
    for i in range(len(input_data)):
        boxes.append(box_process(input_data[i][:,:4,:,:], anchors[i]))
        scores.append(input_data[i][:,4:5,:,:])
        classes_conf.append(input_data[i][:,5:,:,:])

    def sp_flatten(_in):
        ch = _in.shape[1]
        _in = _in.transpose(0,2,3,1)
        return _in.reshape(-1, ch)

    boxes = [sp_flatten(_v) for _v in boxes]
    classes_conf = [sp_flatten(_v) for _v in classes_conf]
    scores = [sp_flatten(_v) for _v in scores]

    boxes = np.concatenate(boxes)
    classes_conf = np.concatenate(classes_conf)
    scores = np.concatenate(scores)

    # filter according to threshold
    boxes, classes, scores = filter_boxes(boxes, scores, classes_conf, obj_thresh)

    # nms
    nboxes, nclasses, nscores = [], [], []
    for c in set(classes):
        inds = np.where(classes == c)
        b = boxes[inds]
        c = classes[inds]
        s = scores[inds]
        keep = nms_boxes(b, s)

        if len(keep) != 0:
            nboxes.append(b[keep])
            nclasses.append(c[keep])
            nscores.append(s[keep])

    if not nclasses and not nscores:
        return None, None, None

    boxes = np.concatenate(nboxes)
    classes = np.concatenate(nclasses)
    scores = np.concatenate(nscores)

    return boxes, classes, scores


def draw(image, boxes, scores, classes, model_names):
    for box, score, cl in zip(boxes, scores, classes):
        top, left, right, bottom = [int(_b) for _b in box]
        print("%s @ (%d %d %d %d) %.3f" % (model_names[cl], top, left, right, bottom, score))
        cv2.rectangle(image, (top, left), (right, bottom), (255, 0, 0), 2)
        cv2.putText(image, '{0} {1:.2f}'.format(model_names[cl], score),
                    (top, left - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    return image

def setup_model(model_path, target, device_id):
    
    platform = ''
    if model_path.endswith('.rknn'):
        platform = 'rknn'
        model = RKNN_model_container(model_path, target, device_id)
    else:
        assert False, "{} is not rknn/pytorch/onnx model".format(model_path)
    logging.error('Model-{} is {} model, starting val'.format(model_path, platform))
    return model, platform




class Detector_N_Drawer_Exist:
    def __init__(self) -> None:
        self.net = ""
        self.smd = ""
        image_shape = 1080  # max width, height parametr
        container_size = 15  # number of images that could be stored
        self.max_size = container_size*image_shape**2
        self.QUEUE_ID = ""
        self.pad_color = (0, 0, 0)
        self.model_im_size = (640, 640)
        self.filter = ''

    def schedule(self, event_input_name, event_input_value, QI, VIS, IMG_ID, QUEUE_ID, MODEL_PTH,  CLASS_PTH, ANCHORS_PTH, TH, FILTRER_CL):
        'Write your code here.'
        if event_input_name == 'INIT':
            sleep(1)
            self.smd = SharedMemoryDict(name=QUEUE_ID, size=self.max_size)
            self.threshold = TH
            self.model, platform = setup_model(MODEL_PTH, 'rk3588', None)
            self.helper = COCO_test_helper(enable_letter_box=True)
            with open(CLASS_PTH, 'r') as f:
                self.names = values = [_v.replace('\n', '') for _v in f.readlines()]

            with open(ANCHORS_PTH, 'r') as f:
                values = [float(_v) for _v in f.readlines()]
                self.anchors = np.array(values).reshape(3,-1,2).tolist()
            logging.error("use anchors from '{}', which is {}".format(ANCHORS_PTH, self.anchors))

            names_output = " ;".join(self.names)
            self.filter = FILTRER_CL.lower()
            
            return event_input_value, None, names_output, True, None, None
        
        if event_input_name == 'REQ':
        #     "Write your handler for current event here."
            q_out = False
            img_id = IMG_ID
            if QI == True:
                img = self.smd[str(IMG_ID)]["image"]
                img_p = img.copy()
                img_p = self.helper.letter_box(im=img_p, new_shape=self.model_im_size, pad_color=self.pad_color)
                img_p = cv2.cvtColor(img_p, cv2.COLOR_BGR2RGB)
                outputs = self.model.run(img_p)
                boxes, classes, scores = post_process(outputs, self.anchors, self.threshold)
                named_classes = []
                if classes is not None:
                    for cl in classes:
                        named_classes.append(self.names[cl])
                if VIS:
                    if boxes is not None:
                        # boxes = self.helper.get_real_box(boxes)
                        img_p = draw(img_p, boxes, scores, classes, self.names)
        #        img_p = cv2.resize(img_p, (1080, 720))
                img_p = cv2.cvtColor(img_p, cv2.COLOR_RGB2BGR)
                cv2.imshow('gfg', img_p)
                cv2.waitKey(1)
                filter_cl_exist = self.filter in named_classes
                q_out = True
                return None, event_input_value, self.names, q_out, img_id, filter_cl_exist
