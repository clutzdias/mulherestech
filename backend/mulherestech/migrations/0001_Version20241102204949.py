from django.db import migrations


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.RunSQL(
            """
            CREATE TABLE usuarios (
              id_usuario uuid DEFAULT uuid_generate_v4(),
              nome varchar(80),
              nome_social varchar(20),
              email varchar(40),
              senha text,
              idade smallint,
              genero varchar(40),
              orientacao_sexual varchar(40),
              data_cadastro datetime without timestamp default now(),
              CONSTRAINT "PK_id_usuario" PRIMARY KEY (id_usuario)
            );
            """,
            "",
        ),
        migrations.RunSQL(
            """
            CREATE TABLE ficha_tecnica (
              id_ficha_tecnica uuid DEFAULT uuid_generate_v4(),
              descricao text,
              nivel varchar(20),
              linguagens text,
              area_atuacao varchar(20),
              link_linkedin varchar(100),
              link_instagram varchar(100),
              link_facebook varchar(100),
              link_tiktok varchar(100),
              link_github varchar(100),
              link_portfolio varchar(100),
              link_outras varchar(100),
              id_usuario uuid NOT NULL,
              CONSTRAINT "PK_id_ficha_tecnica" PRIMARY KEY (id_ficha_tecnica),
              CONSTRAINT "FK_id_usuario_ficha_tecnica" FOREIGN KEY (id_usuario) REFERENCES public.usuarios(id_usuario)

            );
            """,
            "",
        ),
        migrations.RunSQL(
            """
            CREATE TABLE topicos (
              id_topico uuid DEFAULT uuid_generate_v4(),
              titulo varchar(80) not null,
              descricao text,
              curtidas smallint,
              id_usuario uuid not null,
              data_criacao datetime without timestamp default now(),
              CONSTRAINT "PK_id_topico" PRIMARY KEY (id_topico),
	            CONSTRAINT "FK_id_usuario_topico" FOREIGN KEY (id_usuario) REFERENCES public.usuarios(id_usuario)
            );
            """,
            "",
        ),
        migrations.RunSQL(
            """
            CREATE TABLE mensagens (
              id_mensagem uuid DEFAULT uuid_generate_v4(),
              descricao text,
              curtidas smallint,
              id_usuario uuid not null,
              id_topico uuid not null,
              id_mensagem_origem uuid,
              data_criacao datetime without timestamp default now(),
              CONSTRAINT "PK_id_mensagem" PRIMARY KEY (id_mensagem),
	            CONSTRAINT "FK_id_usuario_mensagem" FOREIGN KEY (id_usuario) REFERENCES public.usuarios(id_usuario),
              CONSTRAINT "FK_id_topico_mensagem" FOREIGN KEY (id_topico) REFERENCES public.topicos(id_topico),
              CONSTRAINT "FK_id_mensagem_mensagem_origem" FOREIGN KEY (id_mensagem_origem) REFERENCES public.mensagens(id_mensagem)    
            );
            """,
            "",
        ),
    ]
