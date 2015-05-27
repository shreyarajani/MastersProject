import json, os
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from jobs.query import DataFinder
from models import Season, Episode, Request
import sys
from wsgiref.util import FileWrapper

VIDEOS_URL_PREFIX = 'http://localhost/'
VIDEOS_PATH_PREFIX = 'jobs/requests/'


"""
Redirect from criteria page
and shows seasons
"""


def criteria(request):
    print("criteria page is called")
    seasons = Season.objects.all()

    return render_to_response('criteria.html', {
        'seasons': seasons,
    })


"""
Redirects from selecting the season,
and renders the page
with the episodes from the season number
"""


def results(request):
    # season = request.GET.get('season')
    seasons = [s for s in request.GET.getlist('seasons')]
    print seasons #1,2,3...
    l={}

    for s in seasons: #s=1, s=2
        episodes = Episode.objects.filter(season__id=s)
        l[s] = episodes

    return render_to_response('results.html', {
        'episodes': l,
    })


def results_user(request):
    print "Inside results_user"
    data = request.GET.get('data').encode('ascii')
    print "Data: ", data
    print "Data type: ", type(data)
    j_obj = json.loads(data)
    episodes = j_obj['episodes']
    keyword = (j_obj['keyword'])

    data = json.dumps({"keyword": keyword, "episodes": episodes})
    request_obj = Request(request=data, status="pending")
    request_obj.save()

    return redirect('/requests/?request_id=%d' % request_obj.id)


def intermediate_function(request):
    finderObj = DataFinder()
    keyword = request.GET.get('keyword')
    episodes = [int(ep) for ep in request.GET.getlist('episodes')]  # episode no. here
    print "KEYWORD:", keyword
    print "EPISODES",episodes
    data = json.dumps({"keyword": keyword, "episodes": episodes})
    results1 = finderObj.getDialogueAndTimeStamps(keyword, episodes)  # returns = dialogue_id, episode_id
    print "After requests", results1
    return render_to_response('intermediate.html', {
        'results': results1,
        'data': data,
    })

def requests(request):
    requests = Request.objects.all().order_by('-id')
    return render_to_response('requests.html', {
        'requests': requests,
        'request_id': int(request.GET.get('request_id', 0)),
    })


def request(request, id):
    request_obj = get_object_or_404(Request, id=id)
    return render_to_response('request.html', {
        'request': request_obj,
    })

def download_video(request, request_id):
    request_obj = get_object_or_404(Request, id=request_id)
    file = FileWrapper(open(request_obj.result_path, 'rb'))
    response = HttpResponse(file, content_type='video/mp4')
    filename = os.path.split(request_obj.result_path)[1]
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response

def serve_video(request, request_id):
    request_obj = get_object_or_404(Request, id=request_id)
    path = request_obj.result_path
    index = path.find(VIDEOS_PATH_PREFIX)
    url = VIDEOS_URL_PREFIX + path[index:]
    return redirect(url)
