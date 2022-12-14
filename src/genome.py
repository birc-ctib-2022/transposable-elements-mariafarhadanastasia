"""A circular genome for simulating transposable elements."""

from __future__ import annotations
from typing import (
    Generic, TypeVar, Iterable,
)
from abc import (
    # A tag that says that we can't use this class except by specialising it
    ABC,
    # A tag that says that this method must be implemented by a child class
    abstractmethod
)


class Genome(ABC):
    """Representation of a circular enome."""

    def __init__(self, n: int):
        """Create a genome of size n."""
        ...  # not implemented yet

    @abstractmethod
    def insert_te(self, pos: int, length: int) -> int:
        """
        Insert a new transposable element.

        Insert a new transposable element at position pos and len
        nucleotide forward.

        If the TE collides with an existing TE, i.e. genome[pos]
        already contains TEs, then that TE should be disabled and
        removed from the set of active TEs.

        Returns a new ID for the transposable element.
        """
        ...  # not implemented yet

    @abstractmethod
    def copy_te(self, te: int, offset: int) -> int | None:
        """
        Copy a transposable element.

        Copy the transposable element te to an offset from its current
        location.

        The offset can be positive or negative; if positive the te is copied
        upwards and if negative it is copied downwards. If the offset moves
        the copy left of index 0 or right of the largest index, it should
        wrap around, since the genome is circular.

        If te is not active, return None (and do not copy it).
        """
        ...  # not implemented yet

    @abstractmethod
    def disable_te(self, te: int) -> None:
        """
        Disable a TE.

        If te is an active TE, then make it inactive. Inactive
        TEs are already inactive, so there is no need to do anything
        for those.
        """
        ...  # not implemented yet

    @abstractmethod
    def active_tes(self) -> list[int]:
        """Get the active TE IDs."""
        ...  # not implemented yet

    @abstractmethod
    def __len__(self) -> int:
        """Get the current length of the genome."""
        ...  # not implemented yet

    @abstractmethod
    def __str__(self) -> str:
        """
        Return a string representation of the genome.

        Create a string that represents the genome. By nature, it will be
        linear, but imagine that the last character is immidiatetly followed
        by the first.

        The genome should start at position 0. Locations with no TE should be
        represented with the character '-', active TEs with 'A', and disabled
        TEs with 'x'.
        """
        ...  # not implemented yet


class ListGenome(Genome):
    """
    Representation of a genome.

    Implements the Genome interface using Python's built-in lists
    """

    def __init__(self, n: int):
        """Create a new genome with length n."""
        #initialize the genome with no TE's yet.
        self.genome=(['-']*n)
        self.TE = {}
        self.active = []

    def insert_te(self, pos: int, length: int) -> int:
        """
        Insert a new transposable element.

        Insert a new transposable element at position pos and len
        nucleotide forward.

        If the TE collides with an existing TE, i.e. genome[pos]
        already contains TEs, then that TE should be disabled and
        removed from the set of active TEs.

        Returns a new ID for the transposable element.
        """
        if len(self.TE)==0: 
            ID = 1
        else: 
            ID = max(self.TE) + 1
        self.TE[ID] = length
        self.active.append(ID)
        if pos > 1:
            if isinstance(self.genome[pos-1], int) and isinstance(self.genome[pos], int):
                disable_ID = self.genome[pos]
                self.disable_te(disable_ID)
        self.genome[pos:pos] = [ID]*length
        return ID

    def copy_te(self, te: int, offset: int) -> int | None:
        """
        Copy a transposable element.

        Copy the transposable element te to an offset from its current
        location.

        The offset can be positive or negative; if positive the te is copied
        upwards and if negative it is copied downwards. If the offset moves
        the copy left of index 0 or right of the largest index, it should
        wrap around, since the genome is circular.

        If te is not active, return None (and do not copy it).
        """
        if te not in self.active:
            return None
        for i in range(len(self)):
            if self.genome[i] == te:
                start_orginal_te = i
                break
        start_copy = start_orginal_te + offset
        while start_copy not in range(0, len(self)):
            if start_copy > len(self):
                start_copy = start_copy-len(self)
            if start_copy < 0: 
                start_copy = len(self) + start_copy
        return self.insert_te(start_copy,self.TE[te])
            

    def disable_te(self, te: int) -> None:
        """
        Disable a TE.

        If te is an active TE, then make it inactive. Inactive
        TEs are already inactive, so there is no need to do anything
        for those.
        """
        self.active.remove(te)
        length = self.TE[te]
        for i in range(len(self)):
            if self.genome[i] == te:
                for j in range(i,i+length):
                    self.genome[j] = 'x'
                break

    def active_tes(self) -> list[int]:
        """Get the active TE IDs."""
        return self.active

    def __len__(self) -> int:
        """Current length of the genome."""
        return len(self.genome)

    def __str__(self) -> str:
        """
        Return a string representation of the genome.

        Create a string that represents the genome. By nature, it will be
        linear, but imagine that the last character is immidiatetly followed
        by the first.

        The genome should start at position 0. Locations with no TE should be
        represented with the character '-', active TEs with 'A', and disabled
        TEs with 'x'.
        """
        genome = []
        for x in self.genome:
            if isinstance(x, int):
                genome.append('A')
            else: 
                genome.append(x)
        return "".join(genome)

class Node:
    def __init__(self, te=None, prev = None, next = None):
        self.te = te
        self.prev = prev
        self.next = next

def insert_last(sequence, te):
    new = Node()
    
    new.te = te
    new.next = sequence
    last = sequence.prev
    new.prev = last
    
    sequence.prev = new
    last.next = new

def insert_next(node, te):
    new = Node()
    new.te = te

    new.next = node.next 
    node.next = new
    new.prev = node
    if new.next is not None:
        node.next.prev = new
    


class LinkedListGenome(Genome):
    """
    Representation of a genome.

    Implements the Genome interface using linked lists.
    """

    def __init__(self, n: int):
        """
        Create a new genome with length n.
        
        How we represent genome:
        0: no TEs
        1: active TEs
        2: disabled TEs
        """
        ...  # FIXME

        # Init variables
        self.id = 0 # TEs ID
        self.active = {} # Active TEs e.g. {id1: [start, end], id2: [start, end]}
        self.length = n # Sequence length

        # Initialize first node LinkedList nucleotide
        self.nucleotide = Node(0)
        self.nucleotide.prev = self.nucleotide
        self.nucleotide.next = self.nucleotide
        
        # Insert the nucleotide
        for _ in range(1,n):
            insert_last(self.nucleotide, 0)


    def insert_te(self, pos: int, length: int) -> int:
        """
        Insert a new transposable element.

        Insert a new transposable element at position pos and len
        nucleotide forward.

        If the TE collides with an existing TE, i.e. genome[pos]
        already contains TEs, then that TE should be disabled and
        removed from the set of active TEs.

        Returns a new ID for the transposable element.
        """
        ...  # FIXME
        # Walk to pos
        current = self.nucleotide.prev
        start_index = 0
        if pos < 0:
            pos = self.length + pos
            for _ in range(0,pos):
                current = current.next
                start_index += 1
        else:
            for _ in range(0,pos):
                current = current.next
                start_index += 1

        # Save node after the current
        # to reconnect it again afterwards            
        after = current.next
        
        # Disable active TE if it collides with new TE
        for id, [start_te, end_te] in self.active.items():
            if start_index > start_te and start_index < end_te:
                self.disable_te(id)
                break
        
        # Insert new TE
        for _ in range(length):
            insert_next(current, 1)
            current = current.next
        
        # Reconnect the node
        current.next = after
        after.prev = current
        
        # Update variable
        self.id += 1
        self.length += length
        self.active[self.id] = [start_index, start_index + length - 1]

        # function to update self.active after inserting TEs
        for key, [start, _] in self.active.items():
            if self.id == key:
                pass
            else:
                if start > start_index:
                    self.active[key][0] += length
                    self.active[key][1] += length

        return self.id

    def copy_te(self, te: int, offset: int) -> int | None:
        """
        Copy a transposable element.

        Copy the transposable element te to an offset from its current
        location.

        The offset can be positive or negative; if positive the te is copied
        upwards and if negative it is copied downwards. If the offset moves
        the copy left of index 0 or right of the largest index, it should
        wrap around, since the genome is circular.

        If te is not active, return None (and do not copy it).
        """
        ...  # FIXME
        # Check if TE is active, otherwise return None
        if te not in self.active_tes():
            return None
        
        # Get start_index of the te
        [start, end] = self.active[te]
        length = end - start + 1

        # Walk to start index
        start_index = 0
        current = self.nucleotide.prev
        for _ in range(0,start):
            current = current.next
            start_index += 1

        # Walk to offset
        if offset < 0:
            offset = (self.length +  offset) % self.length
            for _ in range(0,offset):
                current = current.next
            start_index = (start_index + offset) % self.length
        else:
            for _ in range(0,offset):
                current = current.next
            start_index = start_index + offset

        # Save node after the current
        # to reconnect it again afterwards            
        after = current.next
            
        # Disable active TE if it collides with new TE
        for id, [start_te, end_te] in self.active.items():
            if start_index > start_te and start_index < end_te:
                self.disable_te(id)
                break
        
        # Copy TE
        for _ in range(end - start + 1):
            insert_next(current, 1)
            current = current.next

        # Reconnect the node
        current.next = after
        after.prev = current
        
        # Update variable
        self.id += 1
        self.length += length
        self.active[self.id] = [start_index, start_index + length - 1]

        # function to update self.active after inserting TEs
        for key, [start, _] in self.active.items():
            if self.id == key:
                pass
            else:
                if start > start_index:
                    self.active[key][0] += length
                    self.active[key][1] += length

        return self.id

    def disable_te(self, te: int) -> None:
        """
        Disable a TE.

        If te is an active TE, then make it inactive. Inactive
        TEs are already inactive, so there is no need to do anything
        for those.
        """
        ...  # FIXME
        if te in self.active.keys():
            [start, end] = self.active[te]

            # Traverse through the linked list
            current = self.nucleotide.prev

            for _ in range(start + 1):
                current = current.next

            for _ in range(end - start + 1):
                current.te = 2 # disable te
                current = current.next

            del self.active[te] # remove id from self.active

    def active_tes(self) -> list[int]:
        """Get the active TE IDs."""
        # FIXME
        return list(self.active.keys())

    def __len__(self) -> int:
        """Current length of the genome."""
        # FIXME
        return self.length

    def __str__(self) -> str:
        """
        Return a string representation of the genome.

        Create a string that represents the genome. By nature, it will be
        linear, but imagine that the last character is immidiatetly followed
        by the first.

        The genome should start at position 0. Locations with no TE should be
        represented with the character '-', active TEs with 'A', and disabled
        TEs with 'x'.
        """
        node = self.nucleotide
        out = ""

        for _ in range(self.length):
            # out += str(node.te)
            match node.te:
                case 0:
                    out += '-'
                case 1:
                    out += 'A'
                case 2:
                    out += 'x'
            node = node.next
        return out



""" 
The implementation of doubly linked lists from class
"""

T = TypeVar('T')


class Link(Generic[T]):
    """Doubly linked link."""

    val: T
    prev: Link[T]
    next: Link[T]

    def __init__(self, val: T, p: Link[T], n: Link[T]):
        """Create a new link and link up prev and next."""
        self.val = val
        self.prev = p
        self.next = n


def insert_before(link: Link[T], val: T) -> None:
    """Add a new link containing avl after link."""
    new_link = Link(val, link.prev, link)
    new_link.prev.next = new_link
    new_link.next.prev = new_link

def insert_after(link: Link[T], val: T) -> None:
    """Add a new link containing avl before link."""
    new_link = Link(val, link, link.next)
    new_link.prev.next = new_link
    new_link.next.prev = new_link


def remove_link(link: Link[T]) -> None:
    """Remove link from the list."""
    link.prev.next = link.next
    link.next.prev = link.prev


class DLList(Generic[T]):
    """
    Wrapper around a doubly-linked list.

    This is a circular doubly-linked list where we have a
    dummy link that function as both the beginning and end
    of the list. By having it, we remove multiple special
    cases when we manipulate the list.

    >>> x = DLList([1, 2, 3, 4])
    >>> print(x)
    [1, 2, 3, 4]
    """

    head: Link[T]  # Dummy head link

    def __init__(self, seq: Iterable[T] = ()):
        """Create a new circular list from a sequence."""
        # Configure the head link.
        # We are violating the type invariants this one place,
        # but only here, so we ask the checker to just ignore it.
        # Once the head element is configured we promise not to do
        # it again.
        self.head = Link(None, None, None)  # type: ignore
        self.head.prev = self.head
        self.head.next = self.head

        # Add elements to the list, exploiting that self.head.prev
        # is the last element in the list, so appending means inserting
        # after that link.
        for val in seq:
            insert_after(self.head.prev, val)

    def __str__(self) -> str:
        """Get string with the elements going in the next direction."""
        elms: list[str] = []
        link = self.head.next
        while link and link is not self.head:
            elms.append(str(link.val))
            link = link.next
        return f"[{', '.join(elms)}]"
    __repr__ = __str__  # because why not?

class LinkedListGenome2(Genome):
    """
    Representation of a genome.

    Implements the Genome interface using linked lists.
    """

    def __init__(self, n: int):
        """
        Create a new genome with length n.
        """
        self.genome = DLList(['-']*n)
        self.active = []
        self.TE = {}



    def insert_te(self, pos: int, length: int) -> int:
        """
        Insert a new transposable element.

        Insert a new transposable element at position pos and len
        nucleotide forward.

        If the TE collides with an existing TE, i.e. genome[pos]
        already contains TEs, then that TE should be disabled and
        removed from the set of active TEs.

        Returns a new ID for the transposable element.
        """
        if len(self.TE) == 0:
            ID = 1
        else:
            ID = max(self.TE) +1
        self.TE[ID] = length
        self.active.append(ID)
        link = self.genome.head
        
        if pos > 0: 
            link = link.next
            for _ in range(pos): 
                link = link.next 
                if link == self.genome.head:
                    link = link.next
       
        if pos < 0:
            link = link.prev
            for _ in range(abs(pos)): 
                link = link.prev
                if link == self.genome.head:
                    link = link.prev
        
        if link != self.genome.head: 
            if isinstance(link.prev.val, int) and isinstance(link.val, int): 
                self.disable_te(link.val)
        
        if pos < 0: 
            for _ in range(length):
                insert_after(link, ID)
        else:
            for _ in range(length):
                insert_before(link, ID)   


        return ID

    def copy_te(self, te: int, offset: int) -> int | None:
        """
        Copy a transposable element.

        Copy the transposable element te to an offset from its current
        location.

        The offset can be positive or negative; if positive the te is copied
        upwards and if negative it is copied downwards. If the offset moves
        the copy left of index 0 or right of the largest index, it should
        wrap around, since the genome is circular.

        If te is not active, return None (and do not copy it).
        """
        if te not in self.active:
            return None

        link = self.genome.head
        for i in range (len(self)):
            if link.val == te:
                pos = i-1
                break
            link = link.next
        
        return self.insert_te(pos+offset, self.TE[te])

    def disable_te(self, te: int) -> None:
        """
        Disable a TE.

        If te is an active TE, then make it inactive. Inactive
        TEs are already inactive, so there is no need to do anything
        for those.
        """
        link = self.genome.head
        for _ in range(len(self)): 
            link = link.next
            if link.val == te:
                break
        for _ in range(self.TE[te]): 
            link.val = 'x'
            link = link.next
        self.active.remove(te)
        

    def active_tes(self) -> list[int]:
        """Get the active TE IDs."""
        return self.active

    def __len__(self) -> int:
        """Current length of the genome."""
        acc = 0
        link = self.genome.head.next
        while link != self.genome.head:
            acc += 1
            link = link.next
        return acc

    def __str__(self) -> str:
        """
        Return a string representation of the genome.

        Create a string that represents the genome. By nature, it will be
        linear, but imagine that the last character is immidiatetly followed
        by the first.

        The genome should start at position 0. Locations with no TE should be
        represented with the character '-', active TEs with 'A', and disabled
        TEs with 'x'.
        """
        elms: list[str] = []
        link = self.genome.head.next
        while link and link is not self.genome.head:
            if isinstance(link.val,int):
                elms.append('A')
            else:
                elms.append(str(link.val))
            link = link.next
        return "".join(elms) 
