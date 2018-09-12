import graphene
#
# from graphene_django.types import DjangoObjectType
#
# from graphql_demo.ingredients.models import Category, Ingredient
#

# class CategoryType(DjangoObjectType):
#     class Meta:
#         model = Category
#
#
# class IngredientType(DjangoObjectType):
#     class Meta:
#         model = Ingredient
#
#
# class Query(object):
#     all_categories = graphene.List(CategoryType)
#     all_ingredients = graphene.List(IngredientType)
#
#     def resolve_all_categories(self, info, **kwargs):
#         return Category.objects.all()
#
#     def resolve_all_ingredients(self, info, **kwargs):
#         # We can easily optimize query count in the resolve method
#         return Ingredient.objects.select_related('category').all()
#


from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from graphql_demo.ingredients.models import Category, Ingredient


# Graphene will automatically map the Category model's fields onto the CategoryNode.
# This is configured in the CategoryNode's Meta class (as you can see below)
class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = ['name', 'ingredients']
        interfaces = (relay.Node, )


class IngredientNode(DjangoObjectType):
    class Meta:
        model = Ingredient
        # Allow for some more advanced filtering here
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'notes': ['exact', 'icontains'],
            'category': ['exact'],
            'category__name': ['exact'],
        }
        interfaces = (relay.Node, )


class Query(object):
    category = relay.Node.Field(CategoryNode)
    all_categories = DjangoFilterConnectionField(CategoryNode)

    ingredient = relay.Node.Field(IngredientNode)
    all_ingredients = DjangoFilterConnectionField(IngredientNode)


class CreateCategory(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()

    #2
    class Arguments:
        name = graphene.String()

    #3
    def mutate(self, info, name):
        category = Category(name=name)
        category.save()

        return CreateCategory(
            id=category.id,
            name=category.name,
        )


#4
class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
