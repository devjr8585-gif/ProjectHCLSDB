from abc import ABC, abstractmethod

class BaseAdminRepository(ABC):
    @abstractmethod
    def get_all_checklogins(self):
        pass

    @abstractmethod
    def find_checklogin_by_email(self, email):
        pass

    @abstractmethod
    def create_checklogin(self, email, username, password, phone, admin_type, created_by=None, created_at=None):
        pass

    @abstractmethod
    def create_adminlogin_from_check(self, checklogin):
        pass

    @abstractmethod
    def get_opadmin_items_and_counts(self):
        """Return tuple (items_list, active_count, inactive_count) for OpAdmins"""
        pass
