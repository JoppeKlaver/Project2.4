import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { KleurComponent } from './kleur.component';

describe('KleurComponent', () => {
  let component: KleurComponent;
  let fixture: ComponentFixture<KleurComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ KleurComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(KleurComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
