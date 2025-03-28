import os
import magic  # Ensure python-magic is installed
<<<<<<< HEAD
from django.conf import settings
from django.shortcuts import render, redirect
=======
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import PyPDF2
from docx import Document
import requests

from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
>>>>>>> e1dc1b7 (Initial commit)
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

<<<<<<< HEAD
# Import Scikit-learn & FuzzyWuzzy for lightweight AI-based checking
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import fuzz
=======
# Import Scikit-learn & FuzzyWuzzy for AI-based checking
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
>>>>>>> e1dc1b7 (Initial commit)

# Import custom forms and serializers
from .forms import UserRegistrationForm, UserProfileForm
from .serializers import RegisterSerializer, LoginSerializer
<<<<<<< HEAD
from .models import Submission

# Example database of known texts/codes
KNOWN_TEXTS = ["This is an example sentence.", "Another reference text for checking."]
KNOWN_CODES = ["def example_function(): pass", "print('Hello World')"]

# Function to check text plagiarism using TfidfVectorizer
def check_text_plagiarism(text):
    texts = KNOWN_TEXTS + [text]  # Add user text to the database
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    
    similarity_matrix = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    max_score = max(similarity_matrix[0]) if similarity_matrix.size > 0 else 0.0

    report = f"Highest similarity: {max_score * 100:.2f}%."
    return {"similarity_score": max_score, "report": report}

# Function to check code plagiarism using fuzzy matching
def check_code_plagiarism(code):
    max_score = max([fuzz.ratio(code, ref) for ref in KNOWN_CODES]) / 100.0
    report = f"Highest similarity: {max_score * 100:.2f}%."
    return {"similarity_score": max_score, "report": report}

# ---------- REST API Views (for mobile/Flutter clients) ----------
=======
from .models import Submission , Reference

# Expanded database for known texts and codes
KNOWN_TEXTS = ["This is an example sentence.", "Another reference text for checking."]
KNOWN_CODES = ["def example_function(): pass", "print('Hello World')"]

def fetch_internet_references(query):
    # Replace these with your actual API key and search engine ID
    API_KEY = "AIzaSyBaoyFncUauDV33no9aluQ9knb5dDMYi7w"
    CX = "237a688866f8a4d77"
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': API_KEY,
        'cx': CX,
        'q': query,
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json()
        texts = []
        # Extract text snippets from the search results
        for item in results.get('items', []):
            snippet = item.get('snippet', '')
            if snippet:
                texts.append(snippet)
        return texts
    except Exception as e:
        print("Error fetching online references:", e)
        return []

def generate_heatmap(similarity_scores):
    fig, ax = plt.subplots(figsize=(6, 1))
    heatmap_data = np.array([similarity_scores])
    ax.imshow(heatmap_data, cmap="coolwarm", aspect="auto")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Plagiarism Similarity Heatmap")
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode("utf-8")

def check_text_plagiarism(user, input_text):
    # Retrieve persistent references from the Reference model.
    persistent_refs = list(Reference.objects.filter(reference_type='text').values_list('content', flat=True))
    
    # Retrieve local previous text submissions.
    local_texts = list(Submission.objects.filter(submission_type='text').values_list('content', flat=True))
    
    # Use the global known texts as an additional fallback.
    known_texts = KNOWN_TEXTS
    
    # Fetch online references based on the input text.
    online_texts = fetch_internet_references(input_text)
    
    # Combine all available references.
    all_references = persistent_refs + local_texts + known_texts + online_texts

    if all_references:
        # Append the new submission to the reference list for comparison.
        texts = all_references + [input_text]
        vectorizer = TfidfVectorizer(ngram_range=(1, 3))
        tfidf_matrix = vectorizer.fit_transform(texts)
        similarity_matrix = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
        max_similarity = max(similarity_matrix[0]) if similarity_matrix.size > 0 else 0.0
        matched_text = texts[np.argmax(similarity_matrix[0])] if max_similarity > 0 else "No significant match found."
        similarity_score = max_similarity * 100  # Convert to percentage.
        report = f"Highest similarity: {similarity_score:.2f}%."
        heatmap = generate_heatmap(similarity_matrix[0]) if max_similarity > 0 else None
    else:
        similarity_score = 0.0
        matched_text = "No references available for comparison."
        report = "No plagiarism detected (no references found)."
        heatmap = None

    # Save the new submission in your local database for future checks.
    Submission.objects.create(
        user=user,
        content=input_text,
        submission_type='text',
        similarity_score=similarity_score,
        matched_content=matched_text,
    )
    
    return {
        "similarity_score": similarity_score,
        "matched_text": matched_text,
        "report": report,
        "heatmap": heatmap,
        "input_text": input_text,
    }


# Function for code plagiarism detection using FuzzyWuzzy (Levenshtein)
def check_code_plagiarism(user, input_code):
    past_codes = list(Submission.objects.filter(submission_type='code').values_list('content', flat=True))
    
    if past_codes:
        # Compute a similarity score for each past code submission
        scores = [(fuzz.ratio(input_code, code), code) for code in past_codes]
        max_score, matched_code = max(scores, key=lambda x: x[0])
        similarity_score = max_score
        report = f"Highest similarity: {similarity_score:.2f}%."
    else:
        similarity_score = 0.0
        matched_code = "No previous submissions to compare."
        report = "No plagiarism detected (no previous submissions)."
    
    # Store the new code submission
    Submission.objects.create(
        user=user,
        content=input_code,
        submission_type='code',
        similarity_score=similarity_score,
        matched_content=matched_code,
    )
    
    return {
        "similarity_score": similarity_score,
        "matched_code": matched_code,
        "report": report,
        "input_code": input_code,
    }

# ---------- REST API Views ----------
>>>>>>> e1dc1b7 (Initial commit)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"message": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        user = authenticate(username=user.username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "message": "Login successful."
            }, status=status.HTTP_200_OK)
        return Response({"message": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_text_view(request):
    text = request.data.get("text", "")
    if not text:
        return Response({"message": "No text provided."}, status=status.HTTP_400_BAD_REQUEST)
<<<<<<< HEAD
    result = check_text_plagiarism(text)
=======
    
    result = check_text_plagiarism(text)
    
>>>>>>> e1dc1b7 (Initial commit)
    Submission.objects.create(
        user=request.user,
        submission_type="text",
        content=text,
        similarity_score=result["similarity_score"],
        report=result["report"],
    )
<<<<<<< HEAD
=======
    
>>>>>>> e1dc1b7 (Initial commit)
    return Response(result, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_code_view(request):
    code = request.data.get("code", "")
    if not code:
        return Response({"message": "No code provided."}, status=status.HTTP_400_BAD_REQUEST)
<<<<<<< HEAD
    result = check_code_plagiarism(code)
=======
    
    result = check_code_plagiarism(code)
    
>>>>>>> e1dc1b7 (Initial commit)
    Submission.objects.create(
        user=request.user,
        submission_type="code",
        content=code,
        similarity_score=result["similarity_score"],
        report=result["report"],
    )
<<<<<<< HEAD
    return Response(result, status=status.HTTP_200_OK)

# ---------- Website Views ----------
=======
    
    return Response(result, status=status.HTTP_200_OK)

# ---------- Website Views ----------

>>>>>>> e1dc1b7 (Initial commit)
def home_view(request):
    return render(request, 'home.html')

def register_view_web(request):
    if request.user.is_authenticated:
        return redirect('dashboard_web')
    if request.method == "POST":
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('dashboard_web')
        else:
            messages.error(request, "Registration failed. Please try again.")
    else:
        form = UserRegistrationForm()
    return render(request, "register.html", {"form": form})

def login_view_web(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('dashboard_web')
        else:
            messages.error(request, "Invalid credentials. If you don't have an account, please register.")
    else:
        form = AuthenticationForm(request)
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('home')

def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login_web')
    submissions = Submission.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard.html', {'submissions': submissions})

<<<<<<< HEAD
@login_required
def check_view(request):
    result_text = None
    result_code = None
    if request.method == "POST":
        if 'check_text' in request.POST:
            text = request.POST.get("text_input", "").strip()
            uploaded_text_file = request.FILES.get("text_file")
            if uploaded_text_file:
                file_content = uploaded_text_file.read().decode("utf-8", errors="ignore")
                result_text = check_text_plagiarism(file_content)
            elif text:
                result_text = check_text_plagiarism(text)
            Submission.objects.create(
                user=request.user,
                submission_type="text",
                content=text,
                similarity_score=result_text["similarity_score"],
                report=result_text["report"],
            )
        elif 'check_code' in request.POST:
            code = request.POST.get("code_input", "").strip()
            uploaded_code_file = request.FILES.get("code_file")
            if uploaded_code_file:
                file_content = uploaded_code_file.read().decode("utf-8", errors="ignore")
                result_code = check_code_plagiarism(file_content)
            elif code:
                result_code = check_code_plagiarism(code)
            Submission.objects.create(
                user=request.user,
                submission_type="code",
                content=code,
                similarity_score=result_code["similarity_score"],
                report=result_code["report"],
            )
    return render(request, "check.html", {
        "result_text": result_text,
        "result_code": result_code,
    })
=======

def extract_text_from_docx(file):
    """Extract text from a .docx file"""
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_pdf(file):
    """Extract text from a PDF file"""
    pdf_reader = PyPDF2.PdfReader(file)
    return "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])

@login_required
def check_view(request):
    context = {}
    
    if request.method == "POST":
        user = request.user

        # --- TEXT CHECK ---
        if 'check_text' in request.POST:
            input_text = request.POST.get("text_input", "").strip()
            uploaded_files = request.FILES.getlist("text_file")

            if input_text:
                result_text = check_text_plagiarism(user, input_text)
                context["result_text"] = result_text

            elif uploaded_files:
                for file in uploaded_files:
                    try:
                        file_content = None
                        if file.name.endswith(".txt"):
                            file_content = file.read().decode("utf-8", errors="ignore")
                        elif file.name.endswith(".docx"):
                            file_content = extract_text_from_docx(file)
                        elif file.name.endswith(".pdf"):
                            file_content = extract_text_from_pdf(file)

                        if file_content and file_content.strip():
                            result_text = check_text_plagiarism(user, file_content)
                            context["result_text"] = result_text
                            break
                    except Exception as e:
                        print(f"Error processing file {file.name}: {e}")
                        continue

        # --- CODE CHECK ---
        if 'check_code' in request.POST:
            input_code = request.POST.get("code_input", "").strip()
            uploaded_files = request.FILES.getlist("code_file")

            if input_code:
                result_code = check_code_plagiarism(user, input_code)
                context["result_code"] = result_code

            elif uploaded_files:
                for file in uploaded_files:
                    try:
                        file_content = file.read().decode("utf-8", errors="ignore")
                        if file_content.strip():
                            result_code = check_code_plagiarism(user, file_content)
                            context["result_code"] = result_code
                            break
                    except Exception as e:
                        print(f"Error processing file {file.name}: {e}")
                        continue

    return render(request, "check.html", context)


# --- New View for Downloading Report ---
@login_required
def download_report(request):
    # report_type can be "text" or "code"
    report_type = request.GET.get("type", "text")
    # Retrieve the latest submission of the requested type
    submission = Submission.objects.filter(user=request.user, submission_type=report_type).order_by("-created_at").first()
    if not submission:
        return HttpResponse("No report available.", status=404)
    
    # Build the report content (you can customize this format as needed)
    content = f"Report for {report_type.capitalize()} Submission\n\n"
    content += f"Submitted on: {submission.created_at}\n"
    content += f"Similarity Score: {submission.similarity_score:.2f}%\n"
    content += f"Matched Content: {submission.matched_content}\n"
    content += "\n--- Submission Content ---\n"
    content += submission.content
    
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="{report_type}_report.txt"'
    return response

>>>>>>> e1dc1b7 (Initial commit)

@login_required
def profile_view(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile_web')
    else:
        form = UserProfileForm(instance=request.user.profile)
<<<<<<< HEAD
    return render(request, "profile.html", {"form": form})
=======
    return render(request, "profile.html", {"form": form})
>>>>>>> e1dc1b7 (Initial commit)
