import retrieve

print("1. Save objects")
while (object_type := input("Object type to save: ")) != "":
    retrieve.retrieve_and_save(object_type)


# print("2. Import objects")
# import extras
#
#
# print("3. Collate data")
# extras.field
