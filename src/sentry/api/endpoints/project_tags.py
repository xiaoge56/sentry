from __future__ import absolute_import

from rest_framework.response import Response

from sentry.api.bases.project import ProjectEndpoint
from sentry.models import TagKey, TagKeyStatus


class ProjectTagsEndpoint(ProjectEndpoint):
    def get(self, request, project):
        tag_keys = TagKey.objects.filter(
            project=project,
            status=TagKeyStatus.VISIBLE,
        )

        data = []
        for tag_key in tag_keys:
            if tag_key.key.startswith('sentry:'):
                key = tag_key.key.split('sentry:', 1)[-1]
            else:
                key = tag_key.key

            data.append({
                'id': str(tag_key.id),
                'key': key,
                'name': tag_key.get_label(),
                'uniqueValues': tag_key.values_seen,
            })

        return Response(data)
