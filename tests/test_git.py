import mothermayi.git

def test_parse_commit_complete():
    text = ("commit 0fea32abf7ce8aed4038784d7a97df3a615b908e\n"
        "Author:     Eli Ribble <eli@authentise.com>\n"
        "AuthorDate: Mon Nov 23 22:57:08 2015 -0700\n"
        "Commit:     Eli Ribble <eli@authentise.com>\n"
        "CommitDate: Mon Nov 23 22:57:08 2015 -0700\n"
        "\n"
        "Center images horizontally and give them a little space\n"
        "\n"
        "Makes it easier to read my hilarious captions\n"
    )
    commit = mothermayi.git.parse_commit(text)
    expected = {
        'Commit'        : 'Eli Ribble <eli@authentise.com>',
        'commit'        : '0fea32abf7ce8aed4038784d7a97df3a615b908e',
        'Author'        : 'Eli Ribble <eli@authentise.com>',
        'AuthorDate'    : 'Mon Nov 23 22:57:08 2015 -0700',
        'CommitDate'    : 'Mon Nov 23 22:57:08 2015 -0700',
        'Title'         : 'Center images horizontally and give them a little space',
        'Message'       : 'Makes it easier to read my hilarious captions',
    }
    assert commit == expected

def test_parse_commit_without_message():
    text = ("commit 0fea32abf7ce8aed4038784d7a97df3a615b908e\n"
        "Author:     Eli Ribble <eli@authentise.com>\n"
        "AuthorDate: Mon Nov 23 22:57:08 2015 -0700\n"
        "Commit:     Eli Ribble <eli@authentise.com>\n"
        "CommitDate: Mon Nov 23 22:57:08 2015 -0700\n"
        "\n"
        "Center images horizontally and give them a little space\n"
    )
    commit = mothermayi.git.parse_commit(text)
    expected = {
        'Commit'        : 'Eli Ribble <eli@authentise.com>',
        'commit'        : '0fea32abf7ce8aed4038784d7a97df3a615b908e',
        'Author'        : 'Eli Ribble <eli@authentise.com>',
        'AuthorDate'    : 'Mon Nov 23 22:57:08 2015 -0700',
        'CommitDate'    : 'Mon Nov 23 22:57:08 2015 -0700',
        'Title'         : 'Center images horizontally and give them a little space',
        'Message'       : '',
    }
    assert commit == expected

def test_parse_commit_without_separation():
    text = ("commit 0fea32abf7ce8aed4038784d7a97df3a615b908e\n"
        "Author:     Eli Ribble <eli@authentise.com>\n"
        "AuthorDate: Mon Nov 23 22:57:08 2015 -0700\n"
        "Commit:     Eli Ribble <eli@authentise.com>\n"
        "CommitDate: Mon Nov 23 22:57:08 2015 -0700\n"
        "\n"
        "Center images horizontally and give them a little space\n"
        "and do some other stuff with no blank line"
    )
    commit = mothermayi.git.parse_commit(text)
    expected = {
        'Commit'        : 'Eli Ribble <eli@authentise.com>',
        'commit'        : '0fea32abf7ce8aed4038784d7a97df3a615b908e',
        'Author'        : 'Eli Ribble <eli@authentise.com>',
        'AuthorDate'    : 'Mon Nov 23 22:57:08 2015 -0700',
        'CommitDate'    : 'Mon Nov 23 22:57:08 2015 -0700',
        'Title'         : 'Center images horizontally and give them a little space',
        'Message'       : 'and do some other stuff with no blank line',
    }
    assert commit == expected
