from paddles.models import Node
from paddles.tests import TestApp
from paddles import models

from sqlalchemy.exc import StatementError

import pytest


class TestNodeModel(TestApp):

    def test_basic_creation(self):
        Node(name='new_node')
        models.commit()
        assert Node.get(1).name == 'new_node'

    def test_basic_deletion(self):
        new_node = Node('test_basic_deletion')
        models.commit()
        new_node.delete()
        models.commit()
        query = Node.query.filter(Node.name == 'test_basic_deletion')
        assert not query.count()

    def test_init(self):
        name = 'test_init'
        mtype = 'vps'
        Node(name=name, machine_type=mtype)
        models.commit()
        query = Node.query.filter(Node.name == name)\
            .filter(Node.machine_type == mtype)
        assert query.one()

    def test_invalid(self):
        name = 'test_invalid'
        Node(name=name, is_vm='invalid')
        with pytest.raises(StatementError):
            models.commit()
