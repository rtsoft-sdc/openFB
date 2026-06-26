class csvParser:
	def __init__(self):
		self.filenames = []

	def parse_csv(self, FILENAME, FILEORDER):
		try:
			with open(FILENAME, 'r') as file:
				self.filenames = [line.strip() for line in file if line.strip()]
		except Exception as e:
			print(f"Error reading CSV file: {e}")
			self.filenames = []

			return self.filenames[FILEORDER] if 0 <= FILEORDER < len(self.filenames) else None
  
	def get_filenames(self):
		return self.filenames