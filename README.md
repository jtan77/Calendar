The endpoint needs:
- sender_email: string
- recipient_email: string
- title: string
- description: string
- start_date: date time
- end_date: date time
- video_link: string

to be passed in, and I'm not sure what to do with the sender_email, because that's currently the organizer, and the orgainzer will need to be added 
to the google cloud authorized users, otherwise they won't be under the Oauth2 google authorization. 
