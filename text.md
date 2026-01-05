✅ BEST OPTION: MongoDB Time Series Collection (Recommended)

MongoDB has native time-series collections, optimized for exactly this use case.

    Create Time Series Collection
    db.createCollection("temperature_readings", {
    timeseries: {
        timeField: "timestamp",
        metaField: "device",
        granularity: "seconds"
    },
    expireAfterSeconds: 60 * 60 * 24 * 31  // 1 month
    })

    Document Schema
    {
    timestamp: ISODate("2026-01-05T10:00:00Z"),
    device: {
        sensorId: "sensor_01",
        location: "room_1"
    },
    temperature: 24.6,
    unit: "C"
    }

Why this is perfect

✅ Optimized storage (compressed)
✅ Very fast inserts (30 sec interval is ideal)
✅ Built-in TTL cleanup after 1 month
✅ Efficient range queries (last 24h, last week, etc.)

📊 Data Volume (You’re Safe)

1 reading / 30 sec

≈ 2,880 records/day

≈ 86,400 records/month per sensor

MongoDB handles this easily.

🔍 Query Examples
Last 1 hour

    db.temperature_readings.find({
      "device.sensorId": "sensor_01",
      timestamp: { $gte: new Date(Date.now() - 3600 * 1000) }
    })
    
    Average temperature per day
    db.temperature_readings.aggregate([
      { $match: { "device.sensorId": "sensor_01" } },
      {
        $group: {
          _id: {
            $dateToString: { format: "%Y-%m-%d", date: "$timestamp" }
          },
          avgTemp: { $avg: "$temperature" }
        }
      }
    ])

⚠️ If You CAN’T Use Time Series Collections

(Older MongoDB versions)

Normal Collection Schema

    {
      sensorId: "sensor_01",
      temperature: 24.6,
      timestamp: ISODate(),
      expiresAt: ISODate("2026-02-05T00:00:00Z")
    }

    Indexes
    db.temps.createIndex({ timestamp: 1 })
    db.temps.createIndex({ expiresAt: 1 }, { expireAfterSeconds: 0 })

🏆 Final Recommendation

👉 MongoDB ≥ 5.0 → Use time-series collection
👉 Use TTL expiry = 1 month
👉 Store raw readings, compute aggregates on demand or via cron

If you want, tell me:

MongoDB version

Single sensor or multiple sensors?

Do you need hourly/daily aggregates stored too?

I can optimize it even further 🚀

where is the schema?

Good question — MongoDB doesn’t enforce schemas like SQL, so people often get confused here.

Below is the explicit schema definition you can follow (even though MongoDB is schema-less, this is the intended document shape).

✅ Temperature Reading Schema (Time-Series)
Logical Schema (what every document MUST look like)

    TemperatureReading {
      timestamp: Date,            // required (ISODate)
      device: {                   // meta field (indexed automatically)
        sensorId: String,         // required
        location: String          // optional
      },
      temperature: Number,        // required
      unit: String                // optional ("C" or "F")
    }

Example Document

    {
      timestamp: ISODate("2026-01-05T10:00:00Z"),
      device: {
        sensorId: "sensor_01",
        location: "room_1"
      },
      temperature: 24.6,
      unit: "C"
    }

🧱 Enforced Schema (Optional but Recommended)

If you want MongoDB to enforce it, use JSON Schema validation.

Create Collection with Validation

    db.createCollection("temperature_readings", {
      timeseries: {
        timeField: "timestamp",
        metaField: "device",
        granularity: "seconds"
      },
      expireAfterSeconds: 60 * 60 * 24 * 31,
      validator: {
        $jsonSchema: {
          bsonType: "object",
          required: ["timestamp", "device", "temperature"],
          properties: {
            timestamp: {
              bsonType: "date",
              description: "Time of reading"
            },
            device: {
              bsonType: "object",
              required: ["sensorId"],
              properties: {
                sensorId: {
                  bsonType: "string"
                },
                location: {
                  bsonType: "string"
                }
              }
            },
            temperature: {
              bsonType: "number",
              description: "Temperature value"
            },
            unit: {
              bsonType: "string",
              enum: ["C", "F"]
            }
          }
        }
      }
    })
    

Now MongoDB will reject invalid inserts 🚫

📌 Summary

Schema exists → as a document contract

MongoDB doesn’t force it unless you add validation

Time-series collections + JSON Schema = clean + safe

If you want, I can:

Convert this to Mongoose schema

Optimize for multiple sensors

Add hourly/daily aggregation schema

Just tell me 👍

is it like thinkspeak website ?

Yes — exactly like ThingSpeak 👍
What you’re building is essentially a ThingSpeak-style time-series temperature channel, just self-hosted with MongoDB.

Let me map it clearly so it clicks.

🔁 ThingSpeak vs Your MongoDB Setup
🔹 ThingSpeak (conceptually)

Channel = Sensor / Device

Fields = temperature, humidity, etc.

Entry = one reading every X seconds

Time-based charts

Data retention (free tier keeps limited history)

🔹 Your MongoDB Equivalent
ThingSpeak	MongoDB
Channel	sensorId
Field	temperature
Entry	one document
Timestamp	timestamp
Retention	TTL (1 month)
Graphs	frontend (Chart.js, Grafana, etc.)
✅ Your MongoDB Schema (ThingSpeak-like)

    {
      timestamp: ISODate(),
      device: {
        sensorId: "sensor_01"
      },
      temperature: 25.1
    }
    

Stored every 30 seconds, just like ThingSpeak updates.

📊 Example: Same Query as ThingSpeak Chart
“Show last 24 hours”

    db.temperature_readings.find({
      "device.sensorId": "sensor_01",
      timestamp: {
        $gte: new Date(Date.now() - 24 * 60 * 60 * 1000)
      }
    }).sort({ timestamp: 1 })
    

Feed this directly to a line chart.

🏗 Architecture Comparison
ThingSpeak
Sensor → ThingSpeak Cloud → Chart

You
Sensor → API → MongoDB (time-series) → Chart


✔ Full control
✔ No rate limits
✔ No vendor lock-in
✔ Same data model

🔥 Bonus: Multiple Fields (Like ThingSpeak)

If later you want humidity, pressure, etc.:

    {
      timestamp: ISODate(),
      device: { sensorId: "sensor_01" },
      temperature: 25.1,
      humidity: 60.2,
      pressure: 1012
    }


Still valid in a time-series collection.

🏁 Final Answer (Short)

👉 Yes, what you’re designing is functionally the same as ThingSpeak, but you own the backend.

If you want, I can:

Design a ThingSpeak-like REST API

Show Chart.js / Grafana integration

Add channel keys / auth

Just say the word 🚀

give me full schema and example data

Perfect 👍
Below is a complete, clean, ThingSpeak-style MongoDB schema for temperature readings every 30 seconds, stored for 1 month, with example data.

✅ Full MongoDB Schema (Time-Series)
1️⃣ Collection Definition (with validation + TTL)

    db.createCollection("temperature_readings", {
      timeseries: {
        timeField: "timestamp",
        metaField: "meta",
        granularity: "seconds"
      },
      expireAfterSeconds: 60 * 60 * 24 * 31, // 1 month
      validator: {
        $jsonSchema: {
          bsonType: "object",
          required: ["timestamp", "meta", "temperature"],
          properties: {
            timestamp: {
              bsonType: "date",
              description: "Time when temperature was recorded"
            },
            meta: {
              bsonType: "object",
              required: ["sensorId"],
              properties: {
                sensorId: {
                  bsonType: "string",
                  description: "Unique sensor / channel ID"
                },
                location: {
                  bsonType: "string",
                  description: "Physical location of sensor"
                }
              }
            },
            temperature: {
              bsonType: "number",
              description: "Temperature value"
            },
            unit: {
              bsonType: "string",
              enum: ["C", "F"],
              description: "Temperature unit"
            },
            battery: {
              bsonType: "number",
              description: "Battery level percentage"
            }
          }
        }
      }
    })

2️⃣ Document Schema (What Each Record Looks Like)

    TemperatureReading {
      timestamp: Date,
      meta: {
        sensorId: String,
        location?: String
      },
      temperature: Number,
      unit?: "C" | "F",
      battery?: Number
    }

3️⃣ Example Data (Realistic Inserts)
Single Insert

    db.temperature_readings.insertOne({
      timestamp: ISODate("2026-01-05T10:00:00Z"),
      meta: {
        sensorId: "sensor_01",
        location: "living_room"
      },
      temperature: 24.8,
      unit: "C",
      battery: 92
    })

Multiple Readings (Every 30 Seconds)

    db.temperature_readings.insertMany([
      {
        timestamp: ISODate("2026-01-05T10:00:00Z"),
        meta: { sensorId: "sensor_01", location: "living_room" },
        temperature: 24.8,
        unit: "C"
      },
      {
        timestamp: ISODate("2026-01-05T10:00:30Z"),
        meta: { sensorId: "sensor_01", location: "living_room" },
        temperature: 24.9,
        unit: "C"
      },
      {
        timestamp: ISODate("2026-01-05T10:01:00Z"),
        meta: { sensorId: "sensor_01", location: "living_room" },
        temperature: 25.0,
        unit: "C"
      }
    ])

4️⃣ Multiple Sensors (Like Multiple ThingSpeak Channels)

    {
      timestamp: ISODate("2026-01-05T10:00:00Z"),
      meta: {
        sensorId: "sensor_02",
        location: "bedroom"
      },
      temperature: 22.3,
      unit: "C"
    }

5️⃣ Useful Indexes (Optional)

Time-series collections auto-index time + meta, but if needed:

    db.temperature_readings.createIndex({ "meta.sensorId": 1 })

🏁 Final Result

✔ ThingSpeak-style
✔ One record every 30 seconds
✔ Auto-deleted after 1 month
✔ Scales to many sensors
✔ Chart-ready

If you want next:

REST API schema

Mongoose schema

Hourly/daily aggregate collections


Grafana / Chart.js example
