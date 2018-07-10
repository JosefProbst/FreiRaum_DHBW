import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RoomFinderResultsComponent } from './room-finder-results.component';

describe('RoomFinderResultsComponent', () => {
  let component: RoomFinderResultsComponent;
  let fixture: ComponentFixture<RoomFinderResultsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RoomFinderResultsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RoomFinderResultsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
