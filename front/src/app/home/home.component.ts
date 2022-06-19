import { Article } from './../servieces/article.interface';
import { EndpointService } from './../servieces/endpoint.service';
import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import {
  AbstractControl,
  FormBuilder,
  FormControl,
  FormGroup,
  Validators,
} from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';
import { BehaviorSubject } from 'rxjs';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent implements OnInit {
  public form!: FormGroup;
  public articles: Article[] = [];
  public articlesLoaded = new BehaviorSubject<boolean>(false);

  constructor(
    private endpointService: EndpointService,
    private formBuilder: FormBuilder,
    private cdr: ChangeDetectorRef
  ) {}

  private createForms(): void {
    this.form = this.formBuilder.group({
      value: ['', Validators.required],
      idf: new FormControl(false),
      approx: new FormControl(false),
    });
  }

  public convertToFormControl(absCtrl: AbstractControl | null): FormControl {
    return absCtrl as FormControl;
  }

  onSubmit() {
    this.articlesLoaded.next(false);
    this.endpointService.getLinksBySearch(this.form.value).subscribe({
      next: (response: Article[]) => {
        this.articles = response;
        this.articlesLoaded.next(true);
        this.cdr.detectChanges();
      },
      error: (error: HttpErrorResponse) => {
        console.log(error.message);
      },
    });
  }

  ngOnInit(): void {
    this.createForms();
  }
}
