from unittest.mock import MagicMock

import pytest
import qrcode.image.base

import stock_manager
from stock_manager import DatabaseUpdateType, DBUtils, ExportUtils, Item, Logger


class TestDatabase:
    @pytest.fixture
    def database(self) -> DBUtils:
        return DBUtils()
    
    def test_sync_databases(self, database):
        assert database.sync_databases()
    
    def test_fetch_headers(self, database):
        assert database.get_headers()
    
    def test_fetch_data_gs(self, database):
        assert database.get_all_data_gs()
    
    def test_fetch_data_sql(self, database):
        assert database.get_all_data_sql()
    
    def test_fetch_users_gs(self, database):
        assert database.get_all_users_gs()
    
    def test_fetch_users_sql(self, database):
        assert database.get_all_users_sql()
    
    @pytest.mark.parametrize(
            'update_type',
            [
                DatabaseUpdateType.ADD,
                DatabaseUpdateType.EDIT,
                DatabaseUpdateType.REMOVE
            ]
    )
    def test_update_database(self, database, update_type: DatabaseUpdateType):
        assert database.update_items_database(
                update_type, [Item(
                        *['None'] * 3,
                        *[0] * 6,
                        stock_manager.StockStatus.OUT_OF_STOCK.value
                )]
        )
    
    def test_database_notification(self, database):
        assert database.add_notification('test')
    
    def test_already_existing_notif(self, database):
        database.add_notification('test')
        assert database.add_notification('test')
    
    def test_create_items(self, database):
        assert database.create_all_items(database.get_all_data_gs())


class TestLogger:
    @pytest.fixture
    def logger(self) -> Logger:
        return Logger()
    
    def test_info_log(self, logger):
        assert logger.info_log('') is None
    
    def test_warning_log(self, logger):
        assert logger.warning_log('') is None
    
    def test_error_log(self, logger):
        assert logger.error_log('') is None


class TestExports:
    @pytest.fixture
    def exports(self) -> ExportUtils:
        return ExportUtils()
    
    @pytest.mark.parametrize(
            'file_type, expected_path',
            [
                ('py', './exports/py_export.py'),
                ('txt', './exports/txt_export2.txt')
            ]
    )
    def test_valid_name(self, exports, file_type: str, expected_path: str):
        new_path: str = exports._get_valid_name(file_type, './exports')
        assert new_path == expected_path
    
    def test_pdf_export(self, exports):
        pass
    
    @pytest.mark.parametrize('export_type', ['csv', 'tsv', 'psv'])
    def test_sv_export(self, exports, export_type: str):
        assert exports.sv_export(export_type, './exports', [MagicMock()])
    
    def test_make_qr_code(self, exports):
        assert isinstance(exports.create_code('test part'), qrcode.image.base.BaseImage)
    
    def test_save_qr_code(self, exports):
        result: bool = exports.save_code(exports.create_code('test part'), './exports')
        assert result


def test_email_sending():
    assert stock_manager.send_email('Test Email', MagicMock())
