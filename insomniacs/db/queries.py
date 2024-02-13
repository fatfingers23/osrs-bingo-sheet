"""
This module is an attempt at supporting more pythonic approach to mysql queries.

There's probably a better package for doing this, but I'm mostly just tried of blocks of strings for queries.

This was mostly an endeavour what a dev COULD do, as opposed to what a dev SHOULD do.

TODO: Move string/Query definitions outside this module to be constants/functions inside this module
    i.e. Everywhere else in the repo should use something like `SELECT_TEAM_TILES_QUERY` instead of `"SELECT * FROM..."`
"""


class Query(str):
    def __init__(self):
        super().__init__()
        self.tokens = []

    def __str__(self):
        return " ".join(self.tokens) + ";"

    def __call__(self, *args, repeat_previous=False, **kwargs):
        """
        Passing an argument into a call to the object will put the str of the argument as the next token.

        By passing more than 1 argument, the previous token will be repeated e.g.
        `...VARCHAR("FOO", "BAR, "FUZZ", repeat_previous=True)` -> `"VARCHAR FOO VARCHAR BAR VARCHAR FUZZ"`

        :param repeat_previous: Bool, if True the previous token is repeated before each arg
        :param args:
        :param kwargs:
        :return:
        """
        if len(args) == 0:
            return self
        elif len(args) == 1:
            self.tokens.append(str(args[0]))
            return self
        elif len(args) > 1:
            self.tokens.append(str(args[0]))
            if repeat_previous:
                repeat_token = self.tokens[-2]
                self.tokens.append(repeat_token)
            return self(*args[1:])

    @property
    def END(self):
        return str(self)

    @property
    def SELECT(self):
        self.tokens.append("SELECT")
        return self

    @property
    def WHERE(self):
        self.tokens.append("WHERE")
        return self

    @property
    def FROM(self):
        self.tokens.append("FROM")
        return self

    @property
    def ALL(self):
        self.tokens.append("*")
        return self

    @property
    def CREATE(self):
        self.tokens.append("CREATE")
        return self

    @property
    def TABLE(self):
        self.tokens.append("TABLE")
        return self

    @property
    def IF(self):
        self.tokens.append("IF")
        return self

    @property
    def AND(self):
        self.tokens.append("AND")
        return self

    @property
    def EXISTS(self):
        self.tokens.append("EXISTS")
        return self

    @property
    def INSERT(self):
        self.tokens.append("INSERT")
        return self

    @property
    def INTO(self):
        self.tokens.append("INTO")
        return self

    @property
    def VALUES(self):
        self.tokens.append("VALUES")
        return self

    @property
    def INT(self):
        self.tokens.append("INT")
        return self

    @property
    def VARCHAR(self):
        self.tokens.append("VARCHAR")
        return self

    @property
    def DROP(self):
        self.tokens.append("DROP")
        return self

    @property
    def OPEN_P(self):
        self.tokens.append("(")
        return self

    @property
    def CLOSE_P(self):
        self.tokens.append(")")
        return self

    @property
    def COMMA(self):
        self.tokens.append(",")
        return self

    def OPERATOR(self, operator, arg1, arg2):
        """
        For shortcutting operators

        Results in: `<arg1><operator><arg2>`
        """
        self.tokens.append(f"{arg1}{operator}{arg2}")
        return self

    def EQUALS(self, arg1, arg2):
        """
        Creates the statement: <arg1> == <arg2>"

        :param arg1: Left of equal operator
        :param arg2: Right of equal operator
        """
        return self.OPERATOR("=", arg1, arg2)

    @property
    def EQUAL(self):
        self.tokens.append("=")
        return self

    def ENCLOSE(self, arg1, arg2, arg3):
        """
        Adds three strings as one token to prevent spaces between
        <arg1><arg2<arg3>
        """
        self.tokens.append(f"{arg1}{arg2}{arg3}")
        return self

    def QUOTE(self, arg):
        """
        Quotes the argument

        :param arg: The arg to be put in quotes
        """
        return self.ENCLOSE('"', arg, '"')


TEAM_TILE_QUERY = str(Query().
     SELECT.ALL.FROM("bingo_data").WHERE("TeamName").EQUAL("%s")
     )