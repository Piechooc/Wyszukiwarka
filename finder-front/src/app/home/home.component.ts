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

  ngOnInit(): void {
    this.search.valueChanges
      .pipe(
        debounceTime(1000),
        switchMap((value) => of(console.log('Iter ' + value)))
      )
      .subscribe((response) => {
        console.log('Response: ' + response);
      });
  }
}
