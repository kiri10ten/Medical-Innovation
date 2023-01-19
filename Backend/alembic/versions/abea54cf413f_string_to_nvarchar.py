"""String to NVARCHAR

Revision ID: abea54cf413f
Revises: 
Create Date: 2023-01-19 16:07:28.742220

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abea54cf413f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('banner',
    sa.Column('id', sa.Integer(), nullable=False, comment='회사 고유 번호'),
    sa.Column('name', sa.NVARCHAR(length=30), nullable=False, comment='회사명'),
    sa.Column('filename', sa.NVARCHAR(length=40), nullable=False, comment='파일명'),
    sa.Column('link', sa.NVARCHAR(length=100), nullable=False, comment='홈페이지 링크'),
    sa.Column('year', sa.NVARCHAR(length=4), nullable=False, comment='후원 시작 년도'),
    sa.Column('created_at', sa.DateTime(), nullable=False, comment='생성 시점'),
    sa.Column('updated_at', sa.DateTime(), nullable=False, comment='마지막 수정 시점'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    mysql_collate='utf8_general_ci'
    )
    op.create_table('board',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.NVARCHAR(length=20), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False, comment='생성 시점'),
    sa.Column('updated_at', sa.DateTime(), nullable=False, comment='마지막 수정 시점'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    mysql_collate='utf8_general_ci'
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False, comment='유저 고유 번호'),
    sa.Column('name', sa.NVARCHAR(length=20), nullable=False, comment='이름'),
    sa.Column('phone', sa.NVARCHAR(length=20), server_default='01000000000', nullable=True, comment='전화번호'),
    sa.Column('email', sa.NVARCHAR(length=50), nullable=False, comment='이메일 주소 (로그인 아이디)'),
    sa.Column('password', sa.NVARCHAR(length=60), nullable=False, comment='해쉬된 비밀번호'),
    sa.Column('birth', sa.NVARCHAR(length=10), server_default='1900-01-01', nullable=False, comment='생년월일'),
    sa.Column('is_admin', sa.BOOLEAN(), nullable=False, comment='관리자 여부'),
    sa.Column('email_enable', sa.BOOLEAN(), nullable=False, comment='이메일 수신 여부'),
    sa.Column('created_at', sa.DateTime(), nullable=False, comment='생성 시점'),
    sa.Column('updated_at', sa.DateTime(), nullable=False, comment='마지막 수정 시점'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id'),
    mysql_collate='utf8_general_ci'
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.NVARCHAR(length=100), nullable=False),
    sa.Column('board_id', sa.Integer(), nullable=True),
    sa.Column('content', sa.NVARCHAR(length=3000), nullable=False),
    sa.Column('author_name', sa.NVARCHAR(length=20), nullable=True),
    sa.Column('files', sa.NVARCHAR(length=1000), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False, comment='생성 시점'),
    sa.Column('updated_at', sa.DateTime(), nullable=False, comment='마지막 수정 시점'),
    sa.ForeignKeyConstraint(['author_name'], ['user.name'], ),
    sa.ForeignKeyConstraint(['board_id'], ['board.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    mysql_collate='utf8_general_ci'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post')
    op.drop_table('user')
    op.drop_table('board')
    op.drop_table('banner')
    # ### end Alembic commands ###
