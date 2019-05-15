import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs/internal/Observable';
import {environment} from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class FlickrauthService {

  constructor(private http: HttpClient) { }

  private Url = 'https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key='+environment.apiKey+'&tags=bird&format=json&nojsoncallback=1';


  public getHistory():Observable<any> {
    return this.http.get<any>(this.Url);
  }
}
