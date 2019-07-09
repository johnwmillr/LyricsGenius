from api import Genius
genius = Genius("8JuZA2LLElhUEwq_NW25t46s5oLYqjNhTXRoUxKmRENwH8LnWzorrhKl-thRS7E3")

anno = genius.get_song_annotations(873)
print(len(anno))
for a in anno:
    print("\n------------")
    print(a)