import { EndpointService } from './../servieces/endpoint.service';
import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { debounceTime, of, switchMap } from 'rxjs';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit {
  public search = new FormControl('');

  constructor(private endpointService: EndpointService) {}

  ngOnInit(): void {
    this.search.valueChanges
      .pipe(
        debounceTime(1000),
        switchMap((value: string) =>
          this.endpointService.getLinksBySearch(value)
        )
      )
      .subscribe({
        next: (value) => console.log('Response' + value),
        error: (error) => console.log(error),
      });
  }
}
