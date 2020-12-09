
/*
 * Data structure to be stored in TTree representing
 * <constant/> and <variable/> tags.
 */
struct Definition_t {
    Double_t value;
    Char_t   name[128];
};

/*
 * Data structure to be stored in TTree representing
 * <quantity/> scalar type.
 */
struct ComputedQuantity_t {
    Double_t    value;
    Double_t    absoluteValue;
    Char_t      name[128],
                unit[32],
                qType[64]
                ;
};

/*
 * Struct to store vectorial quantities in TFile
 */
struct Vector3_t {
    Double_t    components[3];
    Double_t    computedComponents[3];
    Char_t      name[128], unit[32], qType[32];
};

void
extGDML_nullate_position( Vector3_t & p ) {
    bzero( &p, sizeof( Vector3_t ) );
    strcpy( p.unit, "mm" );
    strcpy( p.qType, "position" );
}

void
extGDML_nullate_rotation( Vector3_t & p ) {
    bzero( &p, sizeof( Vector3_t ) );
    strcpy( p.unit, "rad" );
    strcpy( p.qType, "rotation" );
}

