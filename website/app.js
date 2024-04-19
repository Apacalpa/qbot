const express = require('express');
const session = require('express-session');
const passport = require('passport');
const TwitchStrategy = require('passport-twitch-new').Strategy;  // Use passport-twitch-new
const mysql = require('mysql2');

const db = mysql.createConnection({
    host: '',
    port: ,
    user: '',
    password: '',
    database: ''
});

// Connect to the database
db.connect(function(err) {
    if (err) throw err;
});

passport.use(new TwitchStrategy({  // Use TwitchStrategy
        clientID: '',
        clientSecret: '',
        callbackURL: '',
        scope: ''  // Specify the scope
    },
    function(accessToken, refreshToken, profile, done) {
        return done(null, profile);
    }
));

const app = express();

app.set('view engine', 'ejs')

app.use(session({
    secret: '',
    resave: false,
    saveUninitialized: false
}));

app.use(passport.initialize());
app.use(passport.session());

passport.serializeUser(function(user, done) {
    done(null, user.login);
});

passport.deserializeUser(function(login, done) {
    done(null, login);
});

app.get('/auth/twitch', passport.authenticate('twitch'));  // Simplify the route

app.get('/auth/twitch/callback', passport.authenticate('twitch', { failureRedirect: '/login' }), function(req, res) {
    res.redirect('/');
});

app.get('/', function(req, res) {
    if (req.user) {
        var username = req.user;
        db.query('SELECT * FROM questions WHERE channel = ?', ["#"+username], function(err, results) {
            if (err) throw err;
            res.render('index', { questions: results, user: req.user });
        });
    } else {
        res.render('index', { user: null });
    }
});

app.delete('/questions/:id', function(req, res) {
    var id = req.params.id;

    db.query('DELETE FROM questions WHERE id = ?', [id], function(err, results) {
        if (err) throw err;
        res.send('Question deleted successfully');
    });
});


app.listen(3000, function () {
});
