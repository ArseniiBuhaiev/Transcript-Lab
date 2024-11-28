from transcript import main_phonetic

def test_wop():
    
    word_lst = [
        'спортза!л',
        'сиро!ватці',
        'забу!дься',
        'оселе!дцем',
        'відцура!тися',
        'спрутзасну!в',
        'бу!тси',
        'болі!тце'
    ]

    actual = []
    
    for word in word_lst:
        buffer = main_phonetic(word)
        actual.append(buffer)
    expected = [
        '[сп°орд͡зза́л]',
        '[сиᵉр°о́ва·ц´:і]',
        '[заб°у́·д͡з´с´·а]',
        '[осеᴻле́д͡зцẽᴻм]',
        '[вߴід͡зц°ура́тиᵉс´·а]',
        '[спр°уд͡ззасн°ỹ́ў]',
        '[б°у́цси]',
        '[б°оʸ·л´і́ц:е]'
    ]

    assert actual == expected