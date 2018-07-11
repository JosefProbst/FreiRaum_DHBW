import {Injectable} from '@angular/core';
import {HttpClient, HttpParams} from '@angular/common/http';
import {Observable} from 'rxjs';
import {Lecture} from './models/lecture';
import {Class} from './models/class';
import {Room} from './models/room';

@Injectable({
  providedIn: 'root'
})

// hier werden die Ajax-Abfragen generiert, abgeschickt und deren Antworten empfangen/zurückgegeben
export class HttpService {
  protocol = window.location.protocol;
  hostname = window.location.hostname;

  constructor(
    private http: HttpClient
  ) { }

  // gibt die Vorlesungen der übergebenen Klasse zurück
  getClassPlan(classId: string): Observable<Lecture[]> {
    return this.http.get<Lecture[]>(`${this.protocol}//${this.hostname}:8080/FreiRaum/FreiRaum/1.0.0/classes/${classId}`);
  }

  // gibt eine Liste aller Klassen zurück
  getClasses(): Observable<Class[]> {
    return this.http.get<Class[]>(`${this.protocol}//${this.hostname}:8080/FreiRaum/FreiRaum/1.0.0/classes`);
  }

  // gibt die Belegung des übergebenen Raumes zurück
  getRoomPlan(roomId: string): Observable<Lecture[]> {
    return this.http.get<Lecture[]>(`${this.protocol}//${this.hostname}:8080/FreiRaum/FreiRaum/1.0.0/rooms/${roomId}`);
  }

  // gibt eine Liste aller Räume zurück
  getRooms(): Observable<Room[]> {
    return this.http.get<Room[]>(`${this.protocol}//${this.hostname}:8080/FreiRaum/FreiRaum/1.0.0/rooms`);
  }

  // gibt eine List an Räumen zurück, die im Zeitraum der Parameter frei sind und der ausgewählten Kategorie entsprechen
  getResults(params: HttpParams): Observable<Room[]> {
    return this.http.get<Room[]>(`${this.protocol}//${this.hostname}:8080/FreiRaum/FreiRaum/1.0.0/rooms`, { params: params});
  }
}
