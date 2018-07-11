import {Component, OnInit} from '@angular/core';
import {Room} from '../models/room';
import {Router} from '@angular/router';
import {MatDialog, NativeDateAdapter} from '@angular/material';
import {HttpService} from '../http.service';

@Component({
  selector: 'app-room-finder',
  templateUrl: './room-finder.component.html',
  styleUrls: ['./room-finder.component.css']
})

// hier wird das Formular angezeigt, mit dem nach freien Räumen gesucht werden kann
export class RoomFinderComponent implements OnInit {
  rooms: Room[];
  categories: string[];

  // default Date Variablen
  date = new Date();
  startD = this.date;
  startH = this.date.getHours();
  startM = ('0' + (this.date.getMinutes() - (this.date.getMinutes() % 5))).slice(-2);
  endH = ((this.date.getHours() + 1) === 24) ? 0 : this.date.getHours() + 1;
  endM = this.startM;
  cat = 'all';

  // der gültige Bereich reicht von zwei Wochen in der Vergangenheit bis zwei Wochen in der Zukunft
  minDate = new Date(this.date.getTime() - (14 * 24 * 60 * 60 * 1000));
  maxDate = new Date(this.date.getTime() + (14 * 24 * 60 * 60 * 1000));

  constructor(
    private route: Router,
    private dialog: MatDialog,
    private httpService: HttpService
  ) {}

  // statische Methode um den aktuellen Tag (YYYY-MM-DD) aus dem Date zu holen (bei toISOString gibt es den GMT-Glitch)
  static formatDate(date): string {
    const d = new Date(date);
    let month = '' + (d.getMonth() + 1);
    let day = '' + d.getDate();
    const  year = d.getFullYear();

    if (month.length < 2) { month = '0' + month; }
    if (day.length < 2) { day = '0' + day; }

    return [year, month, day].join('-');
  }

  // beim Laden der Komponente werden alle Räume abgefragt
  ngOnInit() {
    this.httpService.getRooms()
      .subscribe(
        value => this.rooms = value,
        error1 => console.log(error1),
        () => this.getCategories()
      );
  }

  // holt alle Kategorien aus allen Räumen
  getCategories(): void {
    const cats = [];
    for (const c of this.rooms) {
      cats.push(c.category);
    }
    this.categories = Array.from(new Set(cats));
  }

  // interpretiert die eingegebenen User-Daten, navigiert zur Suchergebniskomponente und hängt die User-Daten als Queryparameter an
  // öffnet Fehler-Modal, wenn das Startdatum hinter dem Enddatum liegt
  searchRooms(): void {
    const startTime = new Date((RoomFinderComponent.formatDate
        (this.startD) + 'T' + ('0' + this.startH.toString()).slice(-2) + ':' + this.startM + ':00').toString());
    const endTime = new Date
        ((RoomFinderComponent.formatDate(this.startD) + 'T' + ('0' + this.endH.toString()).slice(-2) + ':' + this.endM + ':00').toString());

    if (startTime < endTime) {
      // noinspection JSIgnoredPromiseFromCall
      this.route.navigate(['/roomFinder/results'], {
        queryParams: {
          starttime: RoomFinderComponent.formatDate(startTime) + 'T' +
              (('0' + startTime.getHours().toString()).slice(-2) + ':' + startTime.getMinutes() + ':00').toString(),
          endtime: RoomFinderComponent.formatDate(endTime) + 'T' +
              (('0' + endTime.getHours().toString()).slice(-2) + ':' + endTime.getMinutes() + ':00').toString(),
          category: this.cat }
      });
    } else {
      this.openDialog();
    }
  }

  // öffnet Fehler-Modal
  openDialog(): void {
    this.dialog.open(RoomFinderDialogComponent, {
      width: '330px'
    });
  }
}

// Deklariert Modal-Komponente
@Component({
  selector: 'app-room-finder-dialog',
  templateUrl: 'room-finder-dialog.html',
})
export class RoomFinderDialogComponent {
  constructor() {}
}

// erstellt Date-Adapter um Methode von NativeDateAdapter zu überschreiben -> Montag soll erster Tag der Woche beim DatePicker sein
export class CustomDateAdapter extends NativeDateAdapter {
  getFirstDayOfWeek(): number {
    return 1;
  }
}
