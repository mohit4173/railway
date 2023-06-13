import json
import random
from fastapi import FastAPI, BackgroundTasks
import asyncio
from starlette.responses import StreamingResponse

app = FastAPI(debug=True)


@app.get('/stream', response_class=StreamingResponse)
async def stream_data():
    async def generate_healthcare_data():
        counter = 1
        num_records = 0
        while num_records < 100:
            record = {}
            action = random.choice(['run', 'sit', 'walk'])
            patient_type = f's{counter}_{action}'
            counter += 1
            if counter > 1000:
                counter = 1
            record['patienttype'] = patient_type
            values = patient_type.split('_')[1:]
            record['values'] = ''.join(values)
            record['Height'] = random.randint(150, 200)
            record['Weight'] = random.randint(40, 150)
            record['Age'] = random.randint(18, 98)
            record['bp_sys_start'] = random.randint(80, 175)
            record['bp_sys_end'] = random.randint(80, 175)
            record['bp_dia_start'] = random.randint(55, 90)
            record['bp_dia_end'] = random.randint(55, 90)
            record['hr_1_start'] = random.randint(50, 120)
            record['hr_1_end'] = random.randint(50, 120)
            record['hr_2_start'] = random.randint(50, 120)
            record['hr_2_end'] = random.randint(50, 120)
            record['spo2_start'] = random.randint(50, 120)
            record['spo2_end'] = random.randint(80, 175)

            yield json.dumps(record) + '\n'
            num_records += 1
            await asyncio.sleep(1)

    async def stream_generator():
        async for data in generate_healthcare_data():
            yield data.encode()  # Add a trailing comma to convert the data to a tuple


    return StreamingResponse(stream_generator(), media_type='text/event-stream')
