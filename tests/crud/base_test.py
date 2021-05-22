from crud.base import CRUDBase
from time import sleep


class TestGetData:

    def test_get_models(self, db_with_add, test_model):
        obj_data = test_model(id=1, name="Test", test_int=112)
        db_with_add.add(obj_data)
        db_with_add.flush()
        retrieved_data = CRUDBase(test_model).get_by_id(db_with_add, 1)
        assert retrieved_data == obj_data

    def test_get_using_filters(self, db_with_add, test_model):
        obj_data = test_model(id=1, name="Test", test_int=112)
        db_with_add.add(obj_data)
        db_with_add.flush()
        filters = {'name': 'Test', 'test_int': 112}
        retrieved_data = CRUDBase(test_model).get(db_with_add, filters)
        assert retrieved_data == obj_data

    def test_get_multi(self, db_with_add, test_model):
        obj_data1 = test_model(id=1, name='Test1', test_int=112)
        obj_data2 = test_model(id=2, name='Test2', test_int=113)
        db_with_add.add(obj_data1)
        db_with_add.add(obj_data2)
        db_with_add.flush()

        filters1 = {'id': 1, 'name': 'Test1'}
        retrieved_data = CRUDBase(test_model).get(db_with_add, filters1)
        assert retrieved_data == obj_data1

        filters2 = {'id': 2, 'name': 'Test2'}
        retrieved_data = CRUDBase(test_model).get(db_with_add, filters2)
        assert retrieved_data == obj_data2


class TestCreateData:

    def test_create(self, db_with_add, test_crud, test_schema):
        obj_in = test_schema(name="test", test_int=999)
        obj_created = test_crud.create(db_with_add, obj_in)

        assert obj_created.name == obj_in.name
        assert obj_created.test_int == obj_in.test_int

        obj_retrieved = test_crud.get(db_with_add, filters={'name': 'test', 'test_int': 999})
        assert obj_retrieved == obj_created

    def test_create_multi(self, db_with_add, test_crud, test_schema):
        obj1 = {'name': 'test1', 'test_int': 999}
        obj2 = {'name': 'test1', 'test_int': 888}
        objs_in = [test_schema(**obj1), test_schema(**obj2)]
        test_crud.create_multi(db_with_add, objs_in)
        obj_retrieved = test_crud.get(db_with_add, obj1)
        assert obj_retrieved.name == obj1['name']
        assert obj_retrieved.test_int == obj1['test_int']

        obj_retrieved = test_crud.get(db_with_add, obj2)
        assert obj_retrieved.name == obj2['name']
        assert obj_retrieved.test_int == obj2['test_int']


class TestUpdateData:

    def test_update_with_dict(self, db_with_add, test_crud, test_schema):
        obj_data = {'name': 'update1', 'test_int': 12}
        updated_obj_data = {'test_int': 21}
        obj_in = test_schema(**obj_data)
        obj_created = test_crud.create(db_with_add, obj_in)
        updated_obj = test_crud.update(db_with_add, obj_created, updated_obj_data)
        assert updated_obj.id == obj_created.id
        assert updated_obj.name == obj_created.name
        assert updated_obj.test_int == updated_obj_data['test_int']
        assert updated_obj.created_at == obj_created.created_at

    def test_update_and_check_if_updated_at_is_changed(
            self, db_with_add, test_crud, test_schema):
        obj_data = {'name': 'update1', 'test_int': 112}
        updated_obj_data = {'test_int': 21}
        obj_in = test_schema(**obj_data)
        obj_created = test_crud.create(db_with_add, obj_in)
        updated_time = obj_created.updated_at
        sleep(1)
        updated_obj = test_crud.update(db_with_add, obj_created, updated_obj_data)
        assert updated_obj.created_at == obj_created.created_at
        assert updated_obj.updated_at != updated_time

    def test_update_with_schema(self, db_with_add, test_crud, test_schema):
        obj_data = {'name': 'update1', 'test_int': 12}
        updated_obj_data = {'name': 'updated1', 'test_int': 21}
        obj_in = test_schema(**obj_data)
        obj_created = test_crud.create(db_with_add, obj_in)
        _id = obj_created.id
        updated_obj_schema = test_schema(**updated_obj_data)
        updated_obj = test_crud.update(db_with_add, obj_created, updated_obj_schema)
        assert updated_obj.id == _id
        assert updated_obj.test_int == updated_obj_schema.test_int

    def test_update_multi(self, db_with_add, test_crud, test_schema):
        obj_data1 = {'name': 'multi1', 'test_int': 1}
        obj_data2 = {'name': 'multi2', 'test_int': 2}

        updated_obj_data1 = {'test_int': 12}
        updated_obj_data2 = {'test_int': 23}

        db_obj1 = test_crud.create(db_with_add, test_schema(**obj_data1))
        db_obj2 = test_crud.create(db_with_add, test_schema(**obj_data2))

        id1 = db_obj1.id
        id2 = db_obj2.id

        obj1 = {'db_obj': db_obj1, 'obj_in': updated_obj_data1}
        obj2 = {'db_obj': db_obj2, 'obj_in': updated_obj_data2}
        objs_in = [obj1, obj2]

        test_crud.update_multi(db_with_add, objs_in)
        retrieved_obj1 = test_crud.get(db_with_add, {'name': 'multi1'})
        assert retrieved_obj1.id == id1
        assert retrieved_obj1.name == obj_data1['name']
        assert retrieved_obj1.test_int == updated_obj_data1['test_int']

        retrieved_obj2 = test_crud.get(db_with_add, {'name': 'multi2'})
        assert retrieved_obj2.id == id2
        assert retrieved_obj2.name == obj_data2['name']
        assert retrieved_obj2.test_int == updated_obj_data2['test_int']

    def test_update_multi_with_schema(self, db_with_add, test_crud, test_schema):
        obj_data1 = {'name': 'multi1', 'test_int': 1}
        obj_data2 = {'name': 'multi2', 'test_int': 2}

        db_obj1 = test_crud.create(db_with_add, test_schema(**obj_data1))
        db_obj2 = test_crud.create(db_with_add, test_schema(**obj_data2))

        id1 = db_obj1.id
        id2 = db_obj2.id

        updated_obj_schema1 = test_schema(**{'name': 'multi1', 'test_int': 12})
        updated_obj_schema2 = test_schema(**{'name': 'multi2', 'test_int': 23})

        obj1 = {'db_obj': db_obj1, 'obj_in': updated_obj_schema1}
        obj2 = {'db_obj': db_obj2, 'obj_in': updated_obj_schema2}
        objs_in = [obj1, obj2]

        test_crud.update_multi(db_with_add, objs_in)
        retrieved_obj1 = test_crud.get_by_id(db_with_add, id1)
        assert retrieved_obj1.id == id1
        assert retrieved_obj1.name == updated_obj_schema1.name
        assert retrieved_obj1.test_int == updated_obj_schema1.test_int

        retrieved_obj2 = test_crud.get_by_id(db_with_add, id2)
        assert retrieved_obj2.id == id2
        assert retrieved_obj2.name == updated_obj_schema2.name
        assert retrieved_obj2.test_int == updated_obj_schema2.test_int


class TestRemoveData:
    def test_remove_single_data_with_id(self, db_with_add, test_crud, test_schema):
        obj_in = test_schema(name="test", test_int=999)
        obj_created = test_crud.create(db_with_add, obj_in)
        _id = obj_created.id
        removed_obj = test_crud.remove_with_id(db_with_add, _id)

        assert removed_obj.id == obj_created.id
        assert test_crud.get_by_id(db_with_add, _id) is None

    def test_remove_multiple_data_with_id(self, db_with_add, test_crud, test_schema):
        obj1 = test_schema(name="test1", test_int=999)
        obj2 = test_schema(name="test2", test_int=888)

        obj_created1 = test_crud.create(db_with_add, obj1)
        obj_created2 = test_crud.create(db_with_add, obj2)
        id1, id2 = (obj_created1.id, obj_created2.id)
        test_crud.remove_multi_with_id(db_with_add, [id1, id2])

        assert test_crud.get_by_id(db_with_add, id1) is None
        assert test_crud.get_by_id(db_with_add, id2) is None

    def test_remove_single_data(self, db_with_add, test_crud, test_schema):
        obj_in = test_schema(name="test", test_int=999)
        obj_created = test_crud.create(db_with_add, obj_in)
        test_crud.remove(db_with_add, obj_created)
        assert test_crud.get_by_id(db_with_add, obj_created.id) is None

    def test_remove_multiple_data(self, db_with_add, test_crud, test_schema):
        obj1 = test_schema(name="test1", test_int=999)
        obj2 = test_schema(name="test2", test_int=888)

        obj_created1 = test_crud.create(db_with_add, obj1)
        obj_created2 = test_crud.create(db_with_add, obj2)
        test_crud.remove_multi(db_with_add, [obj_created1, obj_created2])

        assert test_crud.get_by_id(db_with_add, obj_created1.id) is None
        assert test_crud.get_by_id(db_with_add, obj_created2.id) is None
