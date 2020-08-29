# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import GenericRepr, Snapshot


snapshots = Snapshot()

snapshots['PublicTestSchema::test_mutation_obtain_token 1'] = GenericRepr('<HttpResponse status_code=200, "application/json">')

snapshots['PublicTestSchema::test_mutation_signup 1'] = {
    'data': {
        'signUp': {
            'user': {
                'email': 'new_email@gmail.com',
                'isActive': True
            }
        }
    }
}

snapshots['PublicTestSchema::test_query_user_list 1'] = {
    'data': {
        'userList': {
            'edges': [
                {
                    'node': {
                        'email': 'new_email@gmail.com',
                        'isActive': True
                    }
                }
            ]
        }
    }
}

snapshots['PublicTestSchema::test_mutation_obtain_token_wrong_password 1'] = GenericRepr('<HttpResponse status_code=200, "application/json">')
