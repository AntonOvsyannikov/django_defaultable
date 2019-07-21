# data.py in myapp


def migratedata(apps, schema_editor):
    # defaultables = ['ModelX']
    # defaultables = ['ModelX', 'ModelY']
    defaultables = ['ModelX', 'ModelY', 'ModelZ']

    # owner model, should be after defaults to support squashed migrations over empty database scenario
    Model = apps.get_model('dm', 'Model')
    if not Model.objects.all().exists():
        Model.objects.create()


    for m in defaultables:
        try:
            M = apps.get_model('dm', m)
            if not M.objects.filter(isDefault=True).exists():
                o = M.objects.create(isDefault=True)
                print 'Creating {}:'.format(m), vars(o)
        except LookupError as e:
            print '{} : ignoring'.format(e)

    # try:
    #     ModelZ = apps.get_model('dm', 'ModelZ')
    #     save_to_filefield('CONTENT', ModelZ.objects.get(isDefault=True), 'the_file', 'myfile.txt')
    # except LookupError as e:
    #     print '[{} : ignoring]'.format(e)


