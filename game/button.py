class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image if image is not None else font.render(text_input, True, base_color)
		self.rect = self.image.get_rect(center=pos)
		self.text = font.render(text_input, True, base_color)
		self.text_rect = self.text.get_rect(center=pos)
		self.font = font
		self.base_color = base_color
		self.hovering_color = hovering_color
		self.active = False
		self.text_input = text_input

	def update(self, screen):
		screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def check_for_input(self, position):
		return self.rect.collidepoint(position)

	def hover(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)
