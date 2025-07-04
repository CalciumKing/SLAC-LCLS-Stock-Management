"""
View controller for displaying inventory data in the Stock Management Application.

Handles the main table display and integrates with the database utility.
"""
from functools import partial
from typing import TYPE_CHECKING

from .abstract_controller import AbstractController

if TYPE_CHECKING:
	from stock_manager.app import App


class View(AbstractController):
	"""
	View controller for displaying and managing inventory data.
	"""
	
	def __init__(self, app: 'App'):
		"""
		Initializes the View controller, loads the UI, and sets up the table.
		
		:param app: Reference to the main application instance.
		"""
		
		super().__init__('view', app)
		
		self.update_table(app.all_items, self.table)
		self.search.textChanged.connect(partial(self.filter_table, table=self.table))
		self.export_btn.clicked.connect(lambda: app.screens.setCurrentIndex(1))
