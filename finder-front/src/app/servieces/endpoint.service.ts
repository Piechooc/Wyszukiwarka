import { Article } from './article.interface';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { finderValue } from './finderValue.interface';

@Injectable({
  providedIn: 'root',
})
export class EndpointService {
  public httpUrl = 'http://127.0.0.1:8080/';

  constructor(private http: HttpClient) {}

  public getLinksBySearch(searchValue: finderValue): Observable<Article[]> {
    return this.http.post<Article[]>(this.httpUrl + 'getLinks', searchValue);
  }
}
