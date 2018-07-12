import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';
import { Lecture } from '../models/lecture';
import { HttpService } from '../http.service';

@Component({
  selector: 'app-class',
  templateUrl: './class.component.html',
  styleUrls: ['./class.component.css'],
  encapsulation: ViewEncapsulation.None
})

// hier wird der Kalender des ausgwählten Kurses mit dessen Vorlesungen angezeigt
export class ClassComponent implements OnInit {
  classId: string;
  lectures: Lecture[];

  scheduleOptions: object;
  events: {title: string, description: string, start: string, end: string, color: string}[];

  view = 'normal';

  constructor(
    private route: ActivatedRoute,
    private location: Location,
    private httpService: HttpService
  ) { }

  // beim Laden der Komponente wird der Kurs Parameter abgefragt und es werden die entsprechenden Vorlesungen von der API geholt
  // anschließend werden die Kalenderoptionen gesetzt
  ngOnInit() {
    this.classId = this.route.snapshot.paramMap.get('classId');

    this.httpService.getClassPlan(this.classId)
      .subscribe(
        value => this.lectures = value,
        () => this.view = 'failure',
        () => this.fillScheduleEvents()
      );
    this.setScheduleOptions();
  }

  // führt zur vorherigen Komponente zurück
  goBack(): void {
    this.location.back();
  }

  // setzt die Kalenderoptionen
  setScheduleOptions(): void {
    this.scheduleOptions = {
      // der gültige Bereich reicht vom aktuellen Tag bis 3 Wochen in die Zukunft (um angebrochene Wochen voll anzeigen zu können)
      validRange: {
        start: new Date(),
        end: new Date().getTime() + (21 * 24 * 60 * 60 * 1000)
      },
      weekends: false,
      header: {left: 'prev,next today', center: 'title', right: 'agendaWeek,agendaDay'},
      minTime: '07:00:00',
      maxTime: '22:00:00',
      allDaySlot: false,
      height: 'auto'
    };
  }

  // parst die Vorlesungen in Event-Elemente
  // füllt Event-Array
  fillScheduleEvents(): void {
    const elements = [];

    for (const lecture of this.lectures) {
      const elem = {
        title: lecture.name + ', ' + lecture.roomId,
        start: lecture.startTime,
        end: lecture.endTime,
        color: '#3f51b5' };
      elements.push(elem);
    }
    this.events = elements;
  }
}
