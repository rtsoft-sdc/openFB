from opcua import Client

class PYOPCUA_CLIENT:
	def __init__(self):
		self.client = None
		self.state = ''
		self.dtype = None
		self.node = None
		self.types = {"bool": bool, "int":int}
		self.init_cnt = 0
		self.run_cnt = 0

	def schedule(self, event_input_name, event_input_value, 
			  	QI, URL, NS_ID, NODE_ID, D_TYPE, VALUE):
		state = ''
		qo_out = True
		if event_input_name == "INIT":
			try:
				self.client = Client(url=URL)
				self.client.connect()
				node_id = str(NS_ID) + ";" + str(NODE_ID)
				self.node = self.client.get_node(node_id)
				state = 'Connected to OPC server'
				# TO-DO: Add type casting
				self.dtype = self.types[D_TYPE.lower()]
				self.init_cnt = event_input_value
			except Exception as e:
				print(e)
				state = 'Failed'
				qo_out = False
			print(state)
		elif event_input_name == "RUN":
			if QI == True:
				cur_value = VALUE
				self.node.set_value(cur_value, self.node.get_data_type_as_variant_type())
				state = 'OK'
				self.run_cnt = event_input_value
		self.state = state
		return [self.init_cnt, self.run_cnt, qo_out, self.state]