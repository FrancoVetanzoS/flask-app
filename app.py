from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_migrate import Migrate
from datetime import date, time
from sqlalchemy import Date, Time, Float, String, ForeignKey, Integer
from flask import request, redirect, url_for

#Creamos la aplicación
app=Flask(__name__)

#Conexion a Postgre SQL
USER_DB='postgres'
USER_PASSWORD='123456'
SERVER_DB='localhost'
NAME_DB='TDM2'
FULL_URL_DB=f'postgresql://{USER_DB}:{USER_PASSWORD}@{SERVER_DB}/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI']=FULL_URL_DB

db=SQLAlchemy(app)

#Migracion del modelo
migrate=Migrate()
migrate.init_app(app,db)


#Modelo de datos 1

class AsfaltoMP(db.Model):
    __tablename__ = "AsfaltoMP"

    Cod_MP: Mapped[str] = mapped_column(String(100), primary_key=True)
    fecha: Mapped[date] = mapped_column(Date, nullable=False)
    PEN: Mapped[str] = mapped_column(String(100), nullable=False)

    producciones: Mapped[list["OPEMU"]] = relationship(
        back_populates="asfalto"
    )


class OPEMU(db.Model):
    __tablename__ = "OPEMU"

    Lote: Mapped[str] = mapped_column(String(100), primary_key=True)

    Cod_MP: Mapped[str] = mapped_column(
        String(100),
        ForeignKey("AsfaltoMP.Cod_MP"),
        nullable=False
    )

    Tipo: Mapped[str] = mapped_column(String(100), nullable=False)
    fecha: Mapped[date] = mapped_column(Date, nullable=False)

    asfalto: Mapped["AsfaltoMP"] = relationship(
        back_populates="producciones"
    )

    # 1 a muchos
    parametros: Mapped["ParamEMU"] = relationship(
        back_populates="opemu"
    )

    # 1 a 1
    ensayos: Mapped[list["EnsayoEMU"]] = relationship(
        back_populates="opemu",
        uselist=False
    )


class ParamEMU(db.Model):
    __tablename__ = "param_emu"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    Lote: Mapped[str] = mapped_column(
        String(100),
        ForeignKey("OPEMU.Lote"),
        nullable=False
    )

    Nro: Mapped[int]=mapped_column(Integer)

    RA: Mapped[float] = mapped_column(Float)
    Viscosidad: Mapped[float] = mapped_column(Float)
    Tamiz: Mapped[float] = mapped_column(Float)

    opemu: Mapped["OPEMU"] = relationship(
        back_populates="parametros"
    )


class EnsayoEMU(db.Model):
    __tablename__ = "ensayo_emu"

    Lote: Mapped[str] = mapped_column(
        String(100),
        ForeignKey("OPEMU.Lote"),
        primary_key=True
    )

    RA: Mapped[float] = mapped_column(Float)
    Viscosidad: Mapped[float] = mapped_column(Float)
    Tamiz: Mapped[float] = mapped_column(Float)
    Penetracion: Mapped[float] = mapped_column(Float)

    opemu: Mapped["OPEMU"] = relationship(
        back_populates="ensayos"
    )


###Empezamos con las pagina de inicio

@app.route('/')
def home():
    return render_template('home.html')

#Seguimos con el indice y el registro de MP
@app.route('/MP')
def mp():
    
    fecha = request.args.get('fecha')
    query = AsfaltoMP.query

    if fecha:
        query = query.filter_by(fecha=fecha)

    datos = query.order_by(AsfaltoMP.fecha.desc()).all()
    return render_template('indexMP.html',datos=datos)


@app.route('/MPnuevo', methods=['GET','POST'])
def nuevomp():
    if request.method == 'POST':
        nuevo_registro = AsfaltoMP(
            Cod_MP= request.form['codigomp'],
            fecha= request.form['fecha'],
            PEN= request.form['PEN']
        )
            
        db.session.add(nuevo_registro)
        db.session.commit()
        return redirect(url_for('mp'))
    return render_template('nuevoMP.html')

#Seguimos con el indice y el registro de OP
@app.route('/OP')
def op():
    
    fecha = request.args.get('fecha')
    Lote = request.args.get('Lote')
    query = OPEMU.query

    if fecha:
        query = query.filter_by(fecha=fecha)
    if Lote:
        query = query.filter_by(Lote=Lote)

    datos = query.order_by(OPEMU.fecha.desc()).all()
    return render_template('indexOP.html',datos=datos)


@app.route('/OPnuevo', methods=['GET','POST'])
def nuevoop():
    if request.method == 'POST':
        nuevo_registro = OPEMU(
            Lote= request.form['Lote'],
            Cod_MP= request.form['Cod_MP'],
            Tipo= request.form['Tipo'],
            fecha=request.form['fecha']
        )
            
        db.session.add(nuevo_registro)
        db.session.commit()
        return redirect(url_for('op'))
    return render_template('nuevoOP.html')

#Seguimos con el indice y el registro de CC
@app.route('/CC')
def cc():
    
    Lote = request.args.get('Lote')
    query = ParamEMU.query

    if Lote:
        query = query.filter_by(Lote=Lote)

    datos = query.order_by(ParamEMU.Lote.desc()).all()
    return render_template('indexCC.html',datos=datos)


@app.route('/CCnuevo', methods=['GET','POST'])
def nuevocc():
    if request.method == 'POST':
        nuevo_registro = ParamEMU(
            Lote= request.form['Lote'],
            Nro=request.form['Nro'],
            RA= request.form['RA'],
            Viscosidad=request.form['Viscosidad'],
            Tamiz=request.form['Tamiz']
        )
            
        db.session.add(nuevo_registro)
        db.session.commit()
        return redirect(url_for('cc'))
    return render_template('nuevoCC.html')


#Seguimos con el indice y el registro de IE
@app.route('/IE')
def ie():
    
    Lote = request.args.get('Lote')
    query = EnsayoEMU.query

    if Lote:
        query = query.filter_by(Lote=Lote)

    datos = query.order_by(EnsayoEMU.Lote.desc()).all()
    return render_template('indexIE.html',datos=datos)


@app.route('/IEnuevo', methods=['GET','POST'])
def nuevoie():
    if request.method == 'POST':
        nuevo_registro = EnsayoEMU(
            Lote= request.form['Lote'],
            RA= request.form['RA'],
            Viscosidad=request.form['Viscosidad'],
            Tamiz=request.form['Tamiz'],
            Penetracion=request.form['Penetracion']
        )
            
        db.session.add(nuevo_registro)
        db.session.commit()
        return redirect(url_for('ie'))
    return render_template('nuevoie.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)