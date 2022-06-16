import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class EndpointService {
  public httpUrl = 'http://127.0.0.1:8080/';

  constructor(private http: HttpClient) {}

  public getLinksBySearch(value: string): Observable<any> {
    return this.http.post(this.httpUrl + 'getLinks', value);
  }
}
