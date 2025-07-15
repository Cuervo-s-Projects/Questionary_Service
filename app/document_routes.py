from flask import Blueprint, request, jsonify, Response
from werkzeug.utils import secure_filename
from bson import ObjectId
from .gridfs_utils import GridFSUtils
from .models import Document
from config import Config
from decouple import config
import PyPDF2
import io
import mongoengine

documents_bp = Blueprint('documents', __name__)

try:
    mongoengine.connect(
        db=config('MONGO_DBNAME', default=''),
        host=config('MONGO_URI', default='')
    )
except Exception as e:
    print(f"Error al conectar MongoEngine: {e}")

gridfs_utils = GridFSUtils(db_name=config('MONGO_DBNAME'), mongo_uri=config('MONGO_URI'))

@documents_bp.route('/upload', methods=['POST'])
def upload_document():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Only PDF files are allowed'}), 400
        
        title = request.form.get('title', file.filename)
        description = request.form.get('description', '')
        tags = request.form.get('tags', '').split(',') if request.form.get('tags') else []
        user_id = request.form.get('user_id', 'anonymous')
        
        tags = [tag.strip() for tag in tags if tag.strip()]
        
        filename = secure_filename(file.filename)
        content_type = file.content_type or 'application/pdf'
        
        file.seek(0, 2)
        file_size = str(file.tell())
        file.seek(0)
        
        pages = "1"
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            pages = str(len(pdf_reader.pages))
            file.seek(0)
        except Exception as pdf_error:
            print(f"Error al leer PDF: {pdf_error}")
        
        file_id = gridfs_utils.upload_file(file, filename, content_type)
        
        document = Document(
            title=title,
            description=description,
            tags=tags,
            filename=filename,
            content_type=content_type,
            file_size=file_size,
            user_id=user_id,
            file_id=str(file_id),
            pages=pages
        )
        document.save()
        
        return jsonify({
            'message': 'Document uploaded successfully',
            'document_id': str(document.id),
            'file_id': str(file_id),
            'pages': pages
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@documents_bp.route('/documents/<document_id>', methods=['GET'])
def get_document(document_id):
    try:
        document = Document.objects(id=document_id).first()
        if not document:
            return jsonify({'error': 'Document not found'}), 404
        
        return jsonify(document.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@documents_bp.route('/documents/<document_id>', methods=['DELETE'])
def delete_document(document_id):
    try:
        document = Document.objects(id=document_id).first()
        if not document:
            return jsonify({'error': 'Document not found'}), 404
        
        try:
            gridfs_utils.delete_file(ObjectId(document.file_id))
        except Exception as gridfs_error:
            print(f"Warning: Could not delete file from GridFS: {gridfs_error}")
        
        document.delete()
        
        return jsonify({'message': 'Document deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@documents_bp.route('/download/<file_id>', methods=['GET'])
def download_document(file_id):
    try:
        document = Document.objects(file_id=file_id).first()
        if not document:
            return jsonify({'error': 'Document not found'}), 404
        
        file_id_obj = ObjectId(file_id)
        file_data, content_type = gridfs_utils.download_file(file_id_obj)
        
        filename = document.filename
        
        response = Response(
            file_data,
            mimetype=content_type,
            headers={
                'Content-Disposition': f'attachment; filename="{filename}"',
                'Content-Length': str(len(file_data))
            }
        )
        return response
        
    except Exception as e:
        print(f"Download error: {e}")
        return jsonify({'error': 'File not found or download failed'}), 404

@documents_bp.route('/documents/<document_id>/download', methods=['GET'])
def download_document_by_id(document_id):
    try:
        document = Document.objects(id=document_id).first()
        if not document:
            return jsonify({'error': 'Document not found'}), 404
        
        file_id_obj = ObjectId(document.file_id)
        file_data, content_type = gridfs_utils.download_file(file_id_obj)
        
        response = Response(
            file_data,
            mimetype=content_type,
            headers={
                'Content-Disposition': f'attachment; filename="{document.filename}"',
                'Content-Length': str(len(file_data))
            }
        )
        return response
        
    except Exception as e:
        print(f"Download by ID error: {e}")
        return jsonify({'error': 'File not found or download failed'}), 404

@documents_bp.route('/documents', methods=['GET'])
def list_documents():
    try:
        search_query = request.args.get('search', '')
        tag_filter = request.args.get('tag', '')
        user_filter = request.args.get('user_id', '')
        
        filters = {}
        
        if user_filter:
            filters['user_id'] = user_filter
            
        if tag_filter:
            filters['tags__in'] = [tag_filter]
            
        if search_query:
            from mongoengine import Q
            words = search_query.split()
            search_filter = Q()
            
            for word in words:
                word_filter = Q(title__icontains=word) | Q(description__icontains=word)
                search_filter = search_filter & word_filter if search_filter else word_filter
            
            documents_query = Document.objects(**filters).filter(search_filter)
        else:
            documents_query = Document.objects(**filters)
        
        documents = documents_query.order_by('-upload_date')
        
        documents_list = [document.to_dict() for document in documents]
        
        return jsonify({
            'documents': documents_list,
            'total': len(documents_list)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@documents_bp.route('/documents/search', methods=['GET'])
def search_documents():
    try:
        title = request.args.get('title', '')
        description = request.args.get('description', '')
        tags = request.args.get('tags', '')
        user_id = request.args.get('user_id', '')
        
        query = Document.objects()
        
        if title:
            query = query.filter(title__contains=title)
        if description:
            query = query.filter(description__contains=description)
        if user_id:
            query = query.filter(user_id=user_id)
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',')]
            query = query.filter(tags__in=tag_list)
        
        documents = query.order_by('-upload_date')
        documents_list = [document.to_dict() for document in documents]
        
        return jsonify({
            'documents': documents_list,
            'total': len(documents_list),
            'search_params': {
                'title': title,
                'description': description,
                'tags': tags,
                'user_id': user_id
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
