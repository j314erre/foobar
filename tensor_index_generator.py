
class TensorIndexGenerator():
	"""Iterate through all indices for a tensor
	"""
	
	def __init__(self, dims):
		"""Create the generator.

		Args:
			dims: list with max indices for each tensor dimension
				i.e. [0] is a scalar
					[2] is a 3-vector
					[2,3] is a 3x4 matrix
		"""
		self.dims = dims
		self.rank = len(dims)
		self.hasmore = True
		self.indices = [0]*len(dims)


	def hasMore(self):
		return self.hasmore


	def getNext (self):
		current = list(self.indices)
			
		# increment for next time
		for i in range(self.rank):
			# try to increment
			if self.indices[i]<self.dims[i]:
				self.indices[i] += 1
				break
			else:
				# carry
				self.indices[i] = 0			
				if i==self.rank-1:
					self.hasmore = False	
					
			
		return current
