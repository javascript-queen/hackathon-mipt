from rest_framework import serializers


class NoUpdateFieldsMixin(serializers.ModelSerializer):
    """
    NOTE: is not compatible with write_only=True fields
        as write_only fields are not readable too
    """
    def get_extra_kwargs(self):
        kwargs = super().get_extra_kwargs()
        no_update_fields = getattr(self.__class__.Meta, 'no_update_fields', None)
        if self.instance and no_update_fields:
            for field in no_update_fields:
                kwargs.setdefault(field, {})['read_only'] = True
        return kwargs

    class Meta:
        pass


class HyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer, NoUpdateFieldsMixin):
    pass
