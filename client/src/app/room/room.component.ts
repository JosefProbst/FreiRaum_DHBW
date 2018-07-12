import {Component, OnInit, ViewEncapsulation} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {Location} from '@angular/common';
import {Lecture} from '../models/lecture';
import {HttpService} from '../http.service';

@Component({
  selector: 'app-room',
  templateUrl: './room.component.html',
  styleUrls: ['./room.component.css'],
  encapsulation: ViewEncapsulation.None
})

// hier wird der Kalender des ausgwählten Raumes mit dessen Belegungen angezeigt
export class RoomComponent implements OnInit {
  roomId: string;
  lectures: Lecture[];

  scheduleOptions: object;
  events: { title: string, description: string, start: string, end: string, color: string }[];

  view = 'normal';

  constructor(
    private route: ActivatedRoute,
    private location: Location,
    private httpService: HttpService
  ) { }

  // beim Laden der Komponente wird der Raum Parameter abgefragt und es werden die entsprechenden Belegungen von der API geholt
  // anschließend werden die Kalenderoptionen gesetzt
  ngOnInit() {
    this.roomId = this.route.snapshot.paramMap.get('roomId');

    this.httpService.getRoomPlan(this.roomId)
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
      validRange: {
        // der gültige Bereich reicht vom aktuellen Tag bis 3 Wochen in die Zukunft (um angebrochene Wochen voll anzeigen zu können)
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
        title: lecture.name + ', ' + lecture.classId,
        start: lecture.startTime,
        end: lecture.endTime,
        color: '#3f51b5'
      };
      elements.push(elem);
    }
    this.events = elements;
  }
}
