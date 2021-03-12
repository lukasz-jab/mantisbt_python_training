from sys import maxsize


class Project():
    def __init__(self, name, id=None, status=None, inheritanced=None, visibility=None, description=None):
        self.name = name
        self.id = id
        self.status = status
        self.inheritanced = inheritanced
        self.visibility = visibility
        self.description = description

    def __repr__(self):
        return "%s %s" % (self.id, self.name)

    def __eq__(self, other):
        return (self.id is None or other.id is None or self.id == other.id) and self.name == other.name

    def id_or_max(self):
        if self.id:
            return int(self.id)
        else:
            return maxsize
