repoze.lemonade
===============

repoze.lemonade is a collection of utilties that make it possible to
create Zope CMF-like applications without requiring any particular
persistence mechanism.

Content
-------

The content facilities in ``repoze.lemonade`` are meant to be a
barebones replacement for Zope2 CMF's "types tool".

Content can be registered via ZCML ala:

.. code-block:: xml
   :linenos:

    <configure xmlns="http://namespaces.zope.org/zope"
        xmlns:lemonade="http://namespaces.repoze.org/lemonade"
	               i18n_domain="repoze.lemonade">

      <include package="repoze.lemonade.includes" file="meta.zcml"/>

      <lemonade:content
          factory=".content.Foo"
          type=".content.IFoo"
          />

    </configure>

In the above example, ``factory`` is a class (or function) that
returns an instance of a content class that should implement
``.content.IFoo``.  It can accept positional and keyword arguments as
necessary.  The ``type`` argument signifies that the factory returns
an instance of this type.

Once one or more of these registrations are performed, you can use the
convenience functions in the ``repoze.lemonade.content`` module to
enumerate available content types and to instantiate content objects.
The available API functions in this module are::

  def create_content(iface, *arg, **kw):
      """ Create an instance of the content type related to ``iface``,
          by calling its factory, passing ``*arg`` and ``**kw`` to the factory.
          Raise a ComponentLookupError  if there is no content type related to 
          ``iface`` """

  def get_content_types(context=None):
      """ If ``context`` is None, return a sequence of all registered
          interface objects representing content types available for
          instantiation.  If ``context`` is not None, return a
          sequence of interface objects which are content types which
          are supplied by the context object. """

Only types registered via the ``lemonade:content`` directive are
considered by ``create_content`` and ``get_content_types``.

You will almost certainly want to decorate your content interfaces
with tagged values in order to provide the content type with a name, a
description, an icon, etc, for display in user interfaces.  The zope
interface machinery provides a "tagged values" API that allows you to
do this (you can't just jam attributes onto the interface directly, it
will result in an error).  See `the Zope 3 API documentation
<http://apidoc.zope.org/++apidoc++/Book/ifaceschema/interface/show.html>`_
for more information about setting and retrieving tagged values on
interfaces.  Here's an example:

.. code-block::
   :linenos:

   from zope.interface import Interface
   from zope.interface import taggedValue

   class IMyContentType(Interface):
       taggedValue('name', 'My Content Type')
       taggedValue('description', 'This is a cool content type')

You should then be able to retrieve this metadata after you have a
hold of the content interface via:

.. code-block::
   :linenos:

   IMyContentType.getTaggedValue('name')

The ``IContent`` Interface
--------------------------

When any interface is blessed as a "content" interface via the
``lemonade:content`` ZCML directive, the blessed interface will have
the ``repoze.lemonade.interfaces.IContent`` interface folded into its
``__bases__``.  This means that an object that implements any
interface that has been blessed by ``lemonade:content`` will have
``repoze.lemonade.interfaces.IContent`` in its interface resolution order.

For example, the last expression of the following example code will
return ``True`` if ``IFoo`` has been declared ``lemonade:content`` via
ZCML, and the ZCML has been executed:

.. code-block::
   :linenos:

   from zope.interface import Interface
   from zope.interface import providedBy
   from repoze.lemonade.interfaces import IContent

   class IFoo(Interface):
       pass
   
   class Foo:
       implements(IFoo)

   foo = Foo()
   IContent.providedBy(foo)
   
List Items
----------

A common thing to want to do in an application is to define an
extensible, orderable set of list items that are related to a
particular configuration of software (as opposed to allowing its
composition to be controlled statically within the software itself).
Lemonade provides the ``listitem`` ZCML directive, which permits for
the definition, customization and extension of extensible orderable
sequences.  It uses a (shameful) "sort_key" to provide orderability.

For example:

.. code-block::
   :linenos:

    <configure xmlns="http://namespaces.zope.org/zope"
        xmlns:lemonade="http://namespaces.repoze.org/lemonade"
	               i18n_domain="repoze.lemonade">

    <lemonade:listitem
       provides=".interfaces.IFruit"
       name="peach"
       title="Peach"
       description="A peach is orange and yellow"
       sort_key="10"
       />

    <lemonade:listitem
       provides=".interfaces.IFruit"
       name="apple"
       title="Apple"
       description="Apples are red"
       sort_key="20"
       />

    </configure>

List items are grouped by the interface they ``provide``.  Within each
grouping, the list items belonging to that grouping are sorted by
their respective ``sort_key`` into a list.

Each listitem can also optionally refer to a utility constructor or
component.  This is useful, for instance, if you need to manage a
sequence of factories or other callables.  "Under the hood", each list
item element is registered as a Zope CA utility, so the values to
``factory`, ``component``, ``provides``, and ``name`` have the same
meaning when used as they would if you had used the ``zope:utility``
directive to register a named utility.

.. code-block::
   :linenos:

    <configure xmlns="http://namespaces.zope.org/zope"
        xmlns:lemonade="http://namespaces.repoze.org/lemonade"
	               i18n_domain="repoze.lemonade">

    <lemonade:listitem
       provides=".interfaces.IFruit"
       factory=".fruits.Peach"
       name="peach"
       title="Peach"
       description="arbitrary info about peach"
       sort_key="10"
       />

    <lemonade:listitem
       provides=".interfaces.IFruit"
       factory=".fruits.Apple"
       name="apple"
       title="Apple"
       description="arbitrary info about apple"
       sort_key="20"
       />

    </configure>

As with the ``zope:utility`` directive, instead of using the
``factory`` attribute, the ``component`` attribute may be used if the
utility is already constructed.

.. code-block::
   :linenos:

    <lemonade:listitem
       provides=".interfaces.IFruit"
       component=".fruits.apple"
       name="apple"
       title="Apple"
       description="arbitrary info about apple"
       sort_key="20"
       />

If neither a ``factory`` nor a ``component`` is mentioned, the utility
registration will be performed using the sentinel value ``None`` as
the utility implementation.

The possible attributes of the ``lemonade:listitem`` directive are as
follows:

``provides`` -- A dotted Python name that resolves to an interface.
There is no default, this attribute is required.

``component`` -- A utility component that the listitem is registered for.
If this attribute is specified, the ``factory`` attribute must *not*
be specified.  This attribute is optional.

``factory`` -- A utility factory that the listitem is registered for.
If this attribute is specified, the ``component`` attribute must *not*
be specified.  This attribute is optional.

``name`` -- The name of the listitem.  This is also used as the
utility name when ZCA registry lookup is performed.  This attribute is
required, there is no default.

``title`` -- The title of the listitem.  This attribute defaults to
the empty string.  The value of this element ends up in the utility
registration "info" dict under the key named ``title``.

``description`` -- Arbitrary string information about the listitem.
This attribute defaults to the empty string.  The value of this
element ends up int the utility registration "info" dict under the key
named ``description``.

``sort_key`` -- A string used as a sort key the list items that belong
to a single grouping.  The directive machinery attempts to convert the
string into an integer; if it cannot, however, no error is raised and
the sort key is treated as a string.

Querying for List Items
~~~~~~~~~~~~~~~~~~~~~~~

In your application, you can ask for a sequence of list items
registered against a given interface mentioned as a ``provides``
interface in a ``lemonade:listitem`` directive using the
``get_listitems`` API.  A sequence of dictionaries is returned in
ascending ``sort_key`` order.

.. code-block::
   :linenos:

   >>> from repoze.lemonade.listitem import get_listitems
   >>> from my.package.interfaces import IMyInterface
   >>> listitems = get_listitems(IMyInterface)
   >>> len(listitems)
   2
   >>> listitems[0]
   {'name':'itemname', 'title':'Item Title', 'sort_key':0,
    'component':<function at foo>, 'description':'A description'}

It is not an error to ask for a sequence of list items against an
interface that have no provides registrations; instead, the sequence
of listitems will be empty.

You can also look for a particular utility implied by a list item
using the standard Zope CA ``getUtility`` API::

   >>> from my.package.interfaces import IMyInterface
   >>> utility = getUtility(IMyInterface, name='listitem1')

The ``name`` used in the ``getUtility`` call should be the name of the
listitem.  The value returned will be the instance of a utility
implied by ``factory`` or ``component`` (or ``None`` if neither was
mentioned in the listitem registration).

