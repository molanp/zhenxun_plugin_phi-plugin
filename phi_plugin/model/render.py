from jinja2 import Environment, FileSystemLoader
from nonebot_plugin_alconna import Image
from nonebot_plugin_htmlrender import html_to_pic

from ..components.Config import VERSION
from ..components.pluginPath import imgPath, pluginResources
from .cls.type import tplName

env = Environment(
    loader=FileSystemLoader(pluginResources),
    autoescape=False,
    enable_async=True,
)


async def render(app: tplName, params: dict):
    """渲染 HTML 并转换为图片"""

    template_path = f"html/{app}/{app}.html"
    template = env.get_template(template_path)

    layout_path = "html/common/layout"
    default_layout = f"{layout_path}/default.html"
    elem_layout = f"{layout_path}/elem.html"

    data = {
        **params,
        "tplFile": template_path,
        "_res_path": "",
        "pluResPath": "",
        "_imgPath": str(imgPath.relative_to(pluginResources)),
        "_layout_path": layout_path,
        "defaultLayout": default_layout,
        "elemLayout": elem_layout,
        "sys": {
            "scale": 'style="transform:scale(1)"',
            "copyright": (
                f"Created By phi-Plugin<span class='version'>{VERSION}</span>"
            ),
        },
        "Version": VERSION,
    }

    html_content = await template.render_async(data)
    return Image(
        raw=await html_to_pic(
            html_content, wait=2, template_path=f"file:///{pluginResources}"
        )
    )
