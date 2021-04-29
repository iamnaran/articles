from flask import jsonify
from sqlalchemy import or_, and_

from articles import db
from articles.models.SlangWord import SlangWord
from articles.models.SlangWord import slang_word_schema, slang_words_schema
from articles.models.SlangWordUpVote import SlangWordUpVote, slang_upvote_schema


def get_all_slang():
    all_words = SlangWord.query.all()
    return slang_words_schema.dump(all_words)


def get_slang_by_id(word_id):
    word = SlangWord.query.get(word_id)
    return slang_word_schema.dump(word)


def delete_slang_by_id(post_id):
    post = SlangWord.query.get(post_id)
    return slang_word_schema.dump(post)


def create_new_slang_word(title, content, user_id):
    slang_word = SlangWord(title=title, content=content, user_id=user_id)
    db.session.add(slang_word)
    db.session.commit()
    return slang_word_schema.dump(slang_word)


def upvote_slang(word_id, user_id):
    try:
        post = SlangWordUpVote.query.filter_by(word_id=word_id).filter_by(user_id=user_id).first()

        print(post)

        if post:
            if post.is_liked:
                post.is_liked = False
                db.session.commit()
            else:
                post.is_liked = True
                db.session.commit()

            return slang_upvote_schema.dump(post)

        else:
            post_like = SlangWordUpVote(is_liked=True, word_id=word_id, user_id=user_id)
            db.session.add(post_like)
            db.session.commit()
            return slang_upvote_schema.dump(post_like)

    except Exception as e:
        return False, e.args, "null", "null"
