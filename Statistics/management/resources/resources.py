from import_export import resources, fields

import Statistics.models
import user.models


class MyModelResource(resources.ModelResource):
    class Meta:
        model = Statistics.models.value  # 替换为你的模型
        fields = ('tem', 'humidity', 'time')  # 你想导出的字段
        export_order = ('time', 'tem', 'humidity')  # 导出的字段顺序
