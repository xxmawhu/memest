import time
import hashlib
import configparser

from loguru import logger


def calculate_file_hash(file_path, algorithm="md5"):
    # 创建哈希对象
    hasher = hashlib.new(algorithm)

    # 打开文件并逐块读取数据进行哈希计算
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hasher.update(chunk)

    # 返回哈希值的十六进制表示
    return hasher.hexdigest()


class Config:

    def __init__(self, config_file: str = "config.ini") -> None:
        self.config_file_name = config_file
        cfp = configparser.ConfigParser()
        try:
            cfp.read(self.config_file_name, encoding="utf-8")
        except Exception as e:
            logger.error("fail to read {}, due to {}", self.config_file_name, e)
        self._cfp = cfp
        self.md5_hash = calculate_file_hash(config_file)

    def update_config(self):
        md5_hash = calculate_file_hash(self.config_file_name)
        if md5_hash == self.md5_hash:
            return False

        cfp = configparser.ConfigParser()
        try:
            cfp.read(self.config_file_name, encoding="utf-8")
            self._cfp = cfp
            self.md5_hash = md5_hash
        except Exception as e:
            logger.error("fail to read {}, due to {}", self.config_file_name, e)
        return True

    def get_sections(self):
        return self._cfp.sections()

    def get_value(self, key: str, default_value: str = None) -> str:
        """
        key的格式: section.option

        [section]
        option=value
        """
        if "." in key:
            ll = key.split(".")
            section = ll[0]
            option = ll[1]
            if self._cfp.has_option(section, option):
                return self._cfp.get(section, option).strip('"')
            return default_value
        return default_value

    def get_list(self, key: str, default_value: list = []) -> list:
        """
        key的格式: section.option

        [section]
        option=v1,v2,v3,v4
        @return [v1, v2, v3, v4]
        """
        str_val = self.get_value(key, "")
        if not str_val:
            return default_value
        str_list = [i.strip().strip('"') for i in str_val.split(",") if i.strip()]
        return str_list

    def get_floatlist(self, key: str, default_value: list = []) -> list:
        """
        key的格式: section.option

        [section]
        option=v1,v2,v3,v4
        @return [v1, v2, v3, v4]
        """
        str_val = self.get_value(key, "")
        if not str_val:
            return default_value
        str_list = [float(i.strip()) for i in str_val.split(",") if i.strip()]
        return str_list

    def get_intlist(self, key: str, default_value: list = []) -> list:
        """
        key的格式: section.option

        [section]
        option=v1,v2,v3,v4
        @return [v1, v2, v3, v4]
        """
        str_val = self.get_value(key, "")
        if not str_val:
            return default_value
        str_list = [int(i.strip()) for i in str_val.split(",") if i.strip()]
        return str_list

    def get_floatvalue(self, key: str, default_value: float = None) -> float:
        """
        key的格式: section.option

        [section]
        option=value
        """
        if "." in key:
            ll = key.split(".")
            section = ll[0]
            option = ll[1]
            if self._cfp.has_option(section, option):
                return self._cfp.getfloat(section, option)
            return default_value
        return default_value

    def get_intvalue(self, key: str, default_value: int = None) -> int:
        """
        key的格式: section.option

        [section]
        option=value
        """
        if "." in key:
            ll = key.split(".")
            section = ll[0]
            option = ll[1]
            if self._cfp.has_option(section, option):
                return self._cfp.getint(section, option)
            return default_value
        return default_value

    def get_booleanvalue(self, key: str, default_value: bool = None) -> bool:
        """
        key的格式: section.option

        [section]
        option=value
        """
        if "." in key:
            ll = key.split(".")
            section = ll[0]
            option = ll[1]
            if self._cfp.has_option(section, option):
                return self._cfp.getboolean(section, option)
            return default_value
        return default_value
