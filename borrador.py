
@app.route('/home')
def inicio():

    fecha = request.args.get('fecha')
    nro_orden = request.args.get('nro_orden_prod')

    query = ControlCalidadEmulsion.query

    if fecha:
        query = query.filter_by(fecha_ingreso=fecha)

    if nro_orden:
        query = query.filter_by(nro_orden_prod=nro_orden)

    datos = query.order_by(ControlCalidadEmulsion.id.desc()).all()
    total_registros = len(datos)

    return render_template(
        'indexMP.html',
        total=total_registros,
        datos=datos
    )



@app.route('/nuevoMP', methods=['GET', 'POST'])
def nuevoMP():

    if request.method == 'POST':

        nuevo_registro = ControlCalidadEmulsion(
            fecha_ingreso = request.form['fecha_ingreso'],
            hora = request.form['hora'],
            procedencia = request.form['procedencia'],
            nro_orden_prod = request.form['nro_orden_prod'],
            tipo = request.form['tipo'],
            sbr = request.form['sbr'],
            residuo_asfaltico = request.form['residuo_asfaltico'],
            viscosidad_saybolt = request.form['viscosidad_saybolt'],
            prueba_malla = request.form['prueba_malla'],
            penetracion = request.form['penetracion'],
            punto_ablandamiento = request.form['punto_ablandamiento']
        )

        db.session.add(nuevo_registro)
        db.session.commit()

        return redirect(url_for('inicio'))

    return render_template('nuevo.html')













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

    # 1 a 1
    parametros: Mapped["ParamEMU"] = relationship(
        back_populates="opemu",
        uselist=False
    )

    # 1 a muchos
    ensayos: Mapped[list["EnsayoEMU"]] = relationship(
        back_populates="opemu"
    )


class ParamEMU(db.Model):
    __tablename__ = "param_emu"

    Lote: Mapped[str] = mapped_column(
        String(100),
        ForeignKey("OPEMU.Lote"),
        primary_key=True
    )

    RA: Mapped[float] = mapped_column(Float)
    Viscosidad: Mapped[float] = mapped_column(Float)
    Tamiz: Mapped[float] = mapped_column(Float)

    opemu: Mapped["OPEMU"] = relationship(
        back_populates="parametros"
    )


class EnsayoEMU(db.Model):
    __tablename__ = "ensayo_emu"

    id: Mapped[int] = mapped_column(primary_key=True)

    Lote: Mapped[str] = mapped_column(
        String(100),
        ForeignKey("OPEMU.Lote"),
        nullable=False
    )

    RA: Mapped[float] = mapped_column(Float)
    Viscosidad: Mapped[float] = mapped_column(Float)
    Tamiz: Mapped[float] = mapped_column(Float)
    Penetracion: Mapped[float] = mapped_column(Float)

    opemu: Mapped["OPEMU"] = relationship(
        back_populates="ensayos"
    )

