import random

from django.http import HttpResponse
from django.utils.text import slugify
from faker import Faker
from ..models import Branch, Language, Tag, Relations, User

#binarytree
def array_to_bst(nums, bulk):
    if not nums:
        return None

    mid = len(nums) // 2
    root_id = nums[mid]
    root = Branch.objects.get(pk=root_id)

    child_nums1 = nums[:mid]
    child_nums2 = nums[mid + 1:]

    child1 = array_to_bst(child_nums1, bulk)
    if child1:

        bulk.append(Relations(child=child1, parent=root))


    child2 = array_to_bst(child_nums2,bulk)
    if child2:
        bulk.append(Relations(child=child2, parent=root))

    return root


def fakeitall(req):

    numoftrees=40
    numofbranches = 50


    for j in range(numoftrees):
        fake = Faker()

        #create to get diapason of id
        tile = fake.sentence()
        Branch.objects.bulk_create([
            Branch(title=tile, language=Language.objects.get(name="mghm"),
            author=User.objects.get(pk=1), content=fake.paragraph(), slug=slugify(tile), likes=fake.random_int(min=500, max=5000),
            contentlen=len(tile))]
        )
        last_br=Branch.objects.order_by('-pk').first()
        first_id=last_br.pk+1
        diapasonofid = range(first_id + 1, first_id + numofbranches)




        #creating
        branches =[]
        for i in range(numofbranches):

            title = fake.sentence()
            content = fake.paragraph()
            slug = slugify(title)

            branches.append(Branch(title=title, language=Language.objects.get(name="mghm"),
                                   author=User.objects.get(pk=1), content=content, slug=slug,
                                   likes=fake.random_int(min=500, max=5000), contentlen=len(content)))

        Branch.objects.bulk_create(
            branches
        )

        #create links
        bulk = []
        array_to_bst(diapasonofid, bulk)


        #and another link
        mid = len(diapasonofid) // 2
        root_id = diapasonofid[mid]
        root = Branch.objects.get(pk=root_id)
        bulk.append(Relations(child=root, parent=last_br))
        Relations.objects.bulk_create(
            bulk
        )




    return HttpResponse('succeed')