"""A circular genome for simulating transposable elements."""

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
    new.prev = node
    node.next = new

    node.next.prev = new
    new.next = node.next 


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
        self.active = {} # Active TEs e.g. {id1: [start, length], id2: [start, length]}
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
        # Traverse to index pos
        current = self.nucleotide
        if pos < 0:
            start_index = self.length + 1
            for _ in range(-pos+1):
                current = current.prev
                start_index -= 1

        else:
            start_index = 0
            for _ in range(pos):
                current = current.next
                start_index += 1

        # Temporary save node after the current
        # to reconnect it again afterward            
        after = current.next
        
        # Insert te
        for _ in range(length):
            insert_next(current, 1)
            current = current.next
        
        current.next = after
        after.prev = current
        
        # Update variable
        self.id += 1
        self.length += length
        self.active[self.id] = [start_index, length]

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

    def disable_te(self, te: int) -> None:
        """
        Disable a TE.

        If te is an active TE, then make it inactive. Inactive
        TEs are already inactive, so there is no need to do anything
        for those.
        """
        ...  # FIXME

    def active_tes(self) -> list[int]:
        """Get the active TE IDs."""
        # FIXME
        return self.active

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
            out += str(node.te)
            # match node.te:
            #     case 0:
            #         out += '-'
            #     case 1:
            #         out += 'A'
            #     case 2:
            #         out += 'x'
            node = node.next
        return out