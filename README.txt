repoze.lemonade
===============

repoze.lemonade is a collection of utilties and data structures for
CMF-like applications.

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
   

