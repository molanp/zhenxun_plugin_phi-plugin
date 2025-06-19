from pydantic import BaseModel


class plugin_data(BaseModel):
    money: int
    sign_in: str
    task_time: str
    task: list
    theme: str

class pluginData(BaseModel):
    plugin_data: plugin_data
