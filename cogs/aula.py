from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, Relationship

engine = create_engine('sqlite:///dados.db')
Base = declarative_base()
_Sessao = sessionmaker(engine)

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nome = Column(String(40), unique=True)
    idade = Column(Integer)

    def __repr__(self):
        return f"<{self.nome}>"


class Livro(Base):
    __tablename__ = 'livros'

    id = Column(Integer, primary_key=True)
    nome = Column(String(70))
    ano = Column(Integer)

    autor_id = Column(Integer, ForeignKey('autores.id'))
    autor = Relationship('Autor', backref='livros', lazy='subquery')


class Autor(Base):
    __tablename__ = 'autores'

    id = Column(Integer, primary_key=True)
    nome = Column(String(50))


Base.metadata.create_all(engine)

with _Sessao() as sessao:
    autor = sessao.query(Autor).filter_by(id=1).first()
    for livro in autor.livros:
        print(livro.nome)
