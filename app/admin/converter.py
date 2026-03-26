from typing import Any
from sqlalchemy.orm import ColumnProperty
from sqladmin.forms import converts, ModelConverter as ModelConverterGeneric
from sqladmin.fields import DateTimeField


class ModelConverter(ModelConverterGeneric):

    @converts("TIMESTAMPAware")
    def conv_timestamp_aware(
        self,
        model: type,
        prop: ColumnProperty,
        kwargs: dict[str, Any],
    ):
        return DateTimeField(**kwargs)
